#!/usr/bin/env python3
"""
Continental-Genesis repro screen 19 -- the NO-TUNING THESIS falsifier surface.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, NO fitted parameter; PRESENT-TENSE only; dates/duration RECORD both ways.

Machine-checks the falsifiers of the two architectural claims stated in NO_TUNING_THESIS.md:
  NT-1 (no tuning):   no Tier-A object requires a fitted parameter.
  NT-2 (no addition): every stage is one inherited kernel (c^2=B/rho + R19 switch),
                      not a new mechanism added to clear that stage.

A screen that can only PASS is vacuous. So for every falsifier this screen also evaluates a
COUNTERFACTUAL input that TRIPS the predicate -- proving the test has teeth (it CAN fail). The
verdict per falsifier is SURVIVES (predicate does not fire on measured input) or, for the one
genuinely open item, RESIDUAL-OPEN (the passive model undershoots -> the named next-build task).
Nothing is laundered: F5 is reported open, not as a pass. falsification = discovery.
"""
import hashlib, math

SEED = 19

# ===== LOCK BLOCK (measured present-tense quantities + math constants; no fit) =====
R_EARTH = 6371.0e3           # m
RHO_M   = 3300.0             # kg/m^3  mantle
RHO_W   = 1027.0             # kg/m^3  seawater
RHO_O   = 2900.0             # kg/m^3  oceanic basaltic skin
H_O     = 7.0e3              # m       oceanic crust thickness (measured)
V_W     = 1.335e18           # m^3     total ocean water volume (measured)
OAF     = 0.71               # ocean surface fraction (measured)
RA_MANTLE = 5.85e6           # mantle Rayleigh number (>> critical), present-tense estimate
RA_CRIT   = 27*math.pi**4/4  # free-free onset = 657.5..., analytic constant (validated in solver)
F_COUPLED = 0.30             # two-way-coupled 3D passive-tracer area fraction (executed, v1.3)
F_OBSERVED= 0.41             # observed continental area fraction (measured)
# =================================================================================
A = 4*math.pi*R_EARTH**2

def Etop(H, rho):            # Airy crust-top elevation above a pure-mantle reference
    return H*(RHO_M-rho)/RHO_M

def freeboard(rho_c, H_c, rho_m=RHO_M):
    E_c = H_c*(rho_m-rho_c)/rho_m
    E_o = H_O*(rho_m-RHO_O)/rho_m
    d_w = V_W/(OAF*A)
    SL  = E_o + d_w*(rho_m-RHO_W)/rho_m
    return E_c - SL

L = []
L.append("NO-TUNING THESIS -- falsifier surface (machine-checked; each test carries a counterfactual)")
L.append(f"VP-SPEC  SEED={SEED}  NO fit; present-tense only; dates/duration RECORD both ways")
L.append(f"LOCK rho(m/w/o)={RHO_M:.0f}/{RHO_W:.0f}/{RHO_O:.0f}  H_o={H_O/1e3:.0f}km  V_w={V_W:.3e}  "
         f"Ra={RA_MANTLE:.2e}  Ra_c={RA_CRIT:.1f}  f_coupled={F_COUPLED:.2f}  f_obs={F_OBSERVED:.2f}")
L.append("="*78)
L.append("")
L.append("RULE: a falsifier that cannot fire proves nothing. For each one below, the COUNTERFACTUAL")
L.append("column shows an input that DOES fire it -> the test discriminates. SURVIVES = the measured")
L.append("input does not fire it; RESIDUAL-OPEN = it fires and names the open task (not laundered).")
L.append("")

checks = []  # (label, survives_bool_or_None, counterfactual_fires_bool)

# ---- F1: NT-1 -- does the freeboard fixed point require MOVING rho_c off measured values? ----
OBS_LO, OBS_HI = 300.0, 1200.0     # observed continental freeboard window (m), literature
measured_cfgs = [(2835.0, 30e3), (2870.0, 35e3)]   # measured bulk-crust density/thickness
fb_measured = [(rc, Hc, freeboard(rc, Hc)) for rc, Hc in measured_cfgs]
in_window = [ (OBS_LO <= fb <= OBS_HI) for _,_,fb in fb_measured ]
nt1_survives = any(in_window)       # a MEASURED config lands in-window => no fit forced
fb_textbook = freeboard(2800.0, 35e3)   # the honest 'textbook overshoots' datum
# counterfactual: an observed target no measured value can reach would FORCE a fit
cf_lo, cf_hi = 2500.0, 3000.0
cf_fires_F1 = not any(cf_lo <= fb <= cf_hi for _,_,fb in fb_measured)
L.append("[F1] NT-1 no fitted parameter -- FREEBOARD fixed point (firewall blocks rate x time):")
for rc, Hc, fb in fb_measured:
    L.append(f"     measured rho_c={rc:.0f}, H_c={Hc/1e3:.0f}km -> freeboard {fb:+.0f} m  "
             f"[{'in' if OBS_LO<=fb<=OBS_HI else 'out'} window {OBS_LO:.0f}..{OBS_HI:.0f}]")
L.append(f"     textbook rho_c=2800,35km -> {fb_textbook:+.0f} m (OVERSHOOTS; the param was NOT moved to fit)")
L.append(f"     COUNTERFACTUAL target {cf_lo:.0f}..{cf_hi:.0f} m: no measured rho_c reaches it -> would FORCE a fit (test has teeth: {cf_fires_F1})")
L.append(f"     VERDICT: a MEASURED config lands in observed window -> NT-1 {'SURVIVES' if nt1_survives else 'FALSIFIED'}.  [F]/[V]")
L.append("")
checks.append(("F1", nt1_survives, cf_fires_F1))

# ---- F2: NT-2 -- is the convergence a FORCED limb of the one engine, or an ADDED mechanism? ----
margin = RA_MANTLE/RA_CRIT
nt2_survives = (RA_MANTLE > RA_CRIT)   # Ra>>Ra_c => convection (both limbs) forced by the SAME buoyancy
cf_ra = 100.0
cf_fires_F2 = not (cf_ra > RA_CRIT)    # a sluggish mantle would NOT force convection -> need to ADD a mechanism
L.append("[F2] NT-2 no second engine -- the CONVERGENCE is the forced downwelling limb (M20/CG-36):")
L.append(f"     mantle Ra={RA_MANTLE:.2e}  vs  onset Ra_c=27*pi^4/4={RA_CRIT:.1f}  -> margin {margin:.0f}x")
L.append(f"     Ra>>Ra_c => convection (up+down limbs) is FORCED by the same buoyancy; convergence=downwelling")
L.append(f"     limb, NOT a separate posit. No mechanism is ADDED to obtain it.")
L.append(f"     COUNTERFACTUAL Ra={cf_ra:.0f}<Ra_c: convection NOT forced -> a convergence mechanism would have to")
L.append(f"     be ADDED -> NT-2 would fail (test has teeth: {cf_fires_F2})")
L.append(f"     VERDICT: NT-2 {'SURVIVES' if nt2_survives else 'FALSIFIED'}.  [F]")
L.append("")
checks.append(("F2", nt2_survives, cf_fires_F2))

# ---- F3: the BREAKABLE NUMBER -- freeboard sign + hypsometry order under measured input ----
fb_ref = freeboard(2835.0, 30e3)
ocean_peak = -V_W/(OAF*A)
land_peak  = freeboard(2835.0, 35e3)
separation = land_peak - ocean_peak
sign_ok  = fb_ref > 0.0                       # land EMERGES (correct sign)
order_ok = 3000.0 <= separation <= 7000.0     # two-peak separation right order
f3_survives = sign_ok and order_ok
fb_cf = freeboard(3400.0, 30e3)               # rho_c=3400 > rho_m=3300 -> denser-than-mantle crust
cf_fires_F3 = not (fb_cf > 0.0)               # sign flips -> land would NOT emerge
L.append("[F3] BREAKABLE NUMBER -- present-tense freeboard sign + bimodal-hypsometry order:")
L.append(f"     measured -> freeboard {fb_ref:+.0f} m (sign {'OK' if sign_ok else 'WRONG'}); "
         f"two peaks {land_peak:+.0f}/{ocean_peak:+.0f} m, separation {separation:.0f} m "
         f"(order {'OK' if order_ok else 'WRONG'})")
L.append(f"     COUNTERFACTUAL rho_c=3400>rho_m=3300 -> freeboard {fb_cf:+.0f} m: sign FLIPS, land cannot emerge")
L.append(f"     -> would falsify (test has teeth: {cf_fires_F3})")
L.append(f"     VERDICT: right sign AND right order on measured input -> {'SURVIVES' if f3_survives else 'FALSIFIED'}.  [F]/[V]")
L.append("")
checks.append(("F3", f3_survives, cf_fires_F3))

# ---- F4: CG-24 compensation law -- a COMPENSATED multi-km bare-ocean high would break it ----
# max Airy-compensated relief of a thickened BARE basalt skin (generous: double the crust => dH=H_O)
h_cap_double = H_O*(RHO_M-RHO_O)/RHO_M
h_cap_triple = 2*H_O*(RHO_M-RHO_O)/RHO_M
CAP = 2000.0   # >2 km compensated-bare = the falsifier threshold (well above the ~0.85-1.7 km cap)
# anchors: (name, relief_m, free_air_anomaly_mGal, bare_ocean) -- compensated <=> small FAA
anchors = [("central Indian Ocean", 1500.0,  25.0, True),
           ("Gorringe Bank",        5000.0, 300.0, True)]
def trips_F4(relief, faa):                 # tall AND compensated(=small FAA) over bare skin
    return (relief > CAP) and (faa < 50.0)
f4_survives = not any(trips_F4(r, f) for _,r,f,bare in anchors if bare)
cf_relief, cf_faa = 5000.0, 10.0           # a 5 km bare high WITH small FAA = compensated+tall
cf_fires_F4 = trips_F4(cf_relief, cf_faa)
L.append("[F4] CG-24 compensation law -- max COMPENSATED bare-ocean relief is capped by basalt buoyancy:")
L.append(f"     h_cap = dH*(rho_m-rho_o)/rho_m: double-crust {h_cap_double:.0f} m, triple {h_cap_triple:.0f} m (order ~1 km)")
for nm, r, f, bare in anchors:
    comp = "compensated(small FAA)" if f < 50.0 else "UNcompensated(+FAA, dynamic)"
    L.append(f"     {nm}: relief {r:.0f} m, FAA {f:.0f} mGal -> {comp}; trips falsifier? {trips_F4(r,f)}")
L.append(f"     -> central Indian Ocean sits near the cap (compensated, low); Gorringe is tall but UNcompensated (+FAA).")
L.append(f"     COUNTERFACTUAL: a {cf_relief:.0f} m bare high with FAA {cf_faa:.0f} mGal (tall AND compensated)")
L.append(f"     would break the law (test has teeth: {cf_fires_F4})")
L.append(f"     VERDICT: no compensated multi-km bare-ocean high observed -> {'SURVIVES' if f4_survives else 'FALSIFIED'}.  [F]/[V]")
L.append("")
checks.append(("F4", f4_survives, cf_fires_F4))

# ---- F5: the OPEN residual -- does the PASSIVE coupled model reach observed 0.41? (-> CG-39) ----
gap = F_OBSERVED - F_COUPLED
TOL = 0.03
f5_reaches = (gap <= TOL)              # would the passive model close the value?
f5_residual_open = not f5_reaches     # it does NOT -> residual is real and open
L.append("[F5] OPEN RESIDUAL -- area-fraction VALUE from the passive two-way-coupled model (CG-38 -> CG-39):")
L.append(f"     coupled passive-tracer fraction f={F_COUPLED:.2f}  vs observed {F_OBSERVED:.2f}  -> gap {gap:+.2f} (tol {TOL:.2f})")
L.append(f"     the passive model UNDERSHOOTS (vigorous stirring disperses a passive tracer; real Earth's higher Ra")
L.append(f"     would push it LOWER, not higher). This is NOT laundered into a pass.")
L.append(f"     VERDICT: RESIDUAL-OPEN -- the observed value needs OMITTED physics (continental rheology resisting")
L.append(f"     dispersal + convergent-margin-concentrated production) = the named next-build task CG-39.  [O]/[L]")
L.append(f"     falsification = discovery: the falsification (passive undershoot) IS the discovery (a specific, testable residual).")
L.append("")
checks.append(("F5", None, f5_residual_open))   # survives=None: this one is deliberately OPEN

# ---- self-check: every survivable falsifier has a working counterfactual; F5 is reported open ----
ok = True
L.append("SELF-CHECK (each test must be able to FAIL; the open one must be reported open):")
for label, surv, cf in checks:
    if label == "F5":
        good = (surv is None) and (cf is True)     # correctly OPEN, not a false pass
        tag = "OPEN-REPORTED" if good else "MISLABELLED"
    else:
        good = (surv is True) and (cf is True)      # survives on measured AND counterfactual fires
        tag = "SURVIVES+has-teeth" if good else "VACUOUS-or-FALSIFIED"
    if not good: ok = False
    L.append(f"    [{'OK' if good else 'XX'}] {label}: {tag}")
L.append("")
L.append("VERDICT (firewall-clean): NT-1 and NT-2 survive their falsifiers on MEASURED present-tense")
L.append("input, and each test is non-vacuous (a counterfactual fires it). The single OPEN item is the")
L.append("area-fraction VALUE (0.30<0.41), reported open and routed to CG-39 -- not laundered into a pass.")
L.append("No fitted parameter, no deep-time curve. Occurrence/timing stays [O] forever.")

body = "\n".join(L)
print(body)
assert ok, "a falsifier is vacuous (cannot fire) or the open residual was mislabelled"
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "e50d212e0dd1428fa63f54461e288082b8c461cc4b7da7f8fb5220bbf18e9fac"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
