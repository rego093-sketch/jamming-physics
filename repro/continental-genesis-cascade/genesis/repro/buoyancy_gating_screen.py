#!/usr/bin/env python3
"""
Continental-Genesis repro screen 5 -- buoyant load gates compression.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only; absolute ages RECORD both ways.

Answers the author's map observation: the deep Pacific floor is SMOOTH; only felsic-loaded
crust is crumpled. Mechanism: when a lithospheric column is compressed, its response is gated
by its NET BUOYANCY relative to the asthenosphere,
        B = sum_i (rho_asth - rho_i) * h_i          [kg/m^2]   (x g = upward force/area)
 * B < 0 (negatively buoyant): the column SHEDS compression by SINKING -> SUBDUCTION.
          It does not build thick crumpled topography; its interior stays SMOOTH.
 * B > 0 (positively buoyant): the column CANNOT subduct; compression must THICKEN/FOLD it
          -> CRUMPLE (rough). So crumpling is GATED to buoyant (felsic-loaded) columns.
This is the same composition/buoyancy engine that distils continents (modules 05-06): it now
also explains WHY continents crumple and the bare mantle-skin floor does not. No age is used.
"""
import hashlib

SEED = 19

# ===== LOCK BLOCK (measured/standard densities & thicknesses) =====
RHO_A      = 3300.0   # kg/m^3  asthenospheric mantle (reference)
RHO_OCRUST = 2900.0   # kg/m^3  oceanic basaltic crust
RHO_CCRUST = 2800.0   # kg/m^3  continental (felsic) crust
ALPHA      = 3.0e-5   # 1/K     thermal expansivity of mantle
G          = 9.81     # m/s^2
# column definitions: (crust_rho, crust_h_m, mantle-root thickness_m, root mean cooling dT_K,
#                       root chemical depletion drho_kg_m3 [negative = lighter, e.g. craton])
COLUMNS = {
    "young ocean skin":   (RHO_OCRUST, 7.0e3,  20.0e3, 300.0,   0.0),
    "old ocean skin":     (RHO_OCRUST, 7.0e3,  90.0e3, 600.0,   0.0),
    "felsic continent":   (RHO_CCRUST, 35.0e3, 150.0e3, 600.0, -45.0),  # craton root ~isopycnic
}
# =================================================================

def buoyancy(crust_rho, crust_h, root_h, root_dT, root_depl):
    # crust contribution: (rho_a - rho_crust) * h_crust
    Bc = (RHO_A - crust_rho) * crust_h
    # root contribution: thermal makes it DENSER (anti-buoyant); chemical depletion lighter.
    rho_root = RHO_A * (1.0 + ALPHA * root_dT) + root_depl
    Br = (RHO_A - rho_root) * root_h
    return Bc, Br, Bc + Br

L = []
L.append("BUOYANT LOAD GATES COMPRESSION -- why the deep floor stays smooth")
L.append(f"VP-SPEC  SEED={SEED}  present-tense [F]/[V]; no age, no occurrence")
L.append(f"LOCK  rho_asth={RHO_A:.0f}  rho_ocrust={RHO_OCRUST:.0f}  rho_ccrust={RHO_CCRUST:.0f}  alpha={ALPHA:.0e}/K")
L.append("="*64)
L.append("")
L.append("net buoyancy  B = sum (rho_asth - rho_i) h_i   (>0 = floats/resists subduction)")
L.append("    column               B_crust    B_root      B_net        F_b        response")
for name,(cr,ch,rh,dT,dp) in COLUMNS.items():
    Bc,Br,Bn = buoyancy(cr,ch,rh,dT,dp)
    Fb = G*Bn/1e6   # MPa (upward positive)
    resp = "CRUMPLE (cannot sink -> thicken/fold)" if Bn > 0 else "SUBDUCT (sheds compression by sinking)"
    L.append(f"    {name:<18} {Bc/1e6:8.2f}  {Br/1e6:8.2f}  {Bn/1e6:8.2f} Mkg/m2  {Fb:7.1f} MPa  {resp}")
L.append("    (B in 10^6 kg/m^2; F_b = g*B in MPa, upward positive)")
L.append("")
L.append("READING (firewall-clean):")
L.append("  * old ocean skin is NET NEGATIVE (cold dense root beats the thin light crust)")
L.append("    -> compression is shed by SUBDUCTION; no thick crumpling -> interior SMOOTH.")
L.append("    This is the smooth deep-Pacific floor: bare mantle-skin, not a crumple-able load.")
L.append("  * felsic continent is NET STRONGLY POSITIVE (thick light crust dominates; the")
L.append("    craton root is ~isopycnic) -> it CANNOT subduct -> compression must CRUMPLE it.")
L.append("    So crumpling is GATED to felsic-loaded columns -- exactly where land is.")
L.append("  * young ocean skin is ~neutral/slightly positive (ridges stand high) -> consistent.")
L.append("  * TWO reasons the skin stays smooth, both present-tense: it (a) sheds compression by")
L.append("    subduction (this screen), and (b) is too THIN to buckle into thick relief (module 04).")
L.append("")
L.append("HONEST grade & scope:")
L.append("  * the buoyancy gate is [F] physics; the smooth/crumpled contrast is [V] observation.")
L.append("  * DEGENERATE as a discriminator -- 'continental buoyancy resists subduction' is also")
L.append("    mainstream. Its VALUE here is INTERNAL ECONOMY: the SAME composition/buoyancy engine")
L.append("    that DISTILS continents (M05-06) also gates WHERE crumpling occurs (M04) and why the")
L.append("    bare floor is smooth. One engine, three facts. Grade CG-22: [F]/[V] unifying link.")
L.append("  * rate/when of any compression stays [O] both ways -- unchanged.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "a87f1a89680edae6819fbf1ba53cacbb4ce6a098e1baf9aa6ed322d1e42e51b3"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
