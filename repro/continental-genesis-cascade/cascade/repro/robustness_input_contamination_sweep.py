#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INPUT-CONTAMINATION ROBUSTNESS SWEEP  --  the theory-laden geophysical inputs
=============================================================================
The honest worry (raised directly): some frozen inputs are not observations but
THEORY-LADEN constructs you cannot independently verify -- effective elastic thickness,
mantle density, lithospheric Young's modulus. They carry an ensemble-average model and
may even be quietly corrected toward a standard picture. Auditing every such input to the
bottom is impossible. So the right question is NOT "is the input clean?" but "does the
CONCLUSION depend on the input being clean?".

This screen answers that, for the one place in the cascade where theory-laden geophysical
constants actually flow into a present-tense conclusion: M35's forebulge-position test.
M35 predicts the peripheral forebulge offset from the lithospheric flexural wavelength
  D     = E * Te^3 / (12 (1-nu^2))            (flexural rigidity)
  alpha = (4 D / (rho_m g))^(1/4)             (flexural parameter)
  band  = [0.5*pi*alpha, 1.0*pi*alpha]        (first-forebulge offset band)
and checks the catalogued observed offsets (US Mid-Atlantic 300 km, North Sea 250 km)
against a tolerance-widened band [0.6*lo, 1.4*hi].

alpha scales as  E^(1/4) * Te^(3/4) * rho_m^(-1/4) * (1-nu^2)^(-1/4)  -- Te dominates.

METHOD (no tuning; pre-registered contamination ranges from the literature spread):
  Te    in [40, 100] km   (cratonic effective elastic thickness; baseline 70)
  E     in [50, 100] GPa  (lithospheric Young's modulus; baseline 70)
  rho_m in [3200, 3400]   (mantle density; baseline 3300)
  nu    in [0.20, 0.30]   (Poisson ratio; baseline 0.25)
We sweep the full grid (including all worst-case corners), test whether BOTH observed
offsets stay bracketed at EVERY grid point, and then locate the exact Te survival window
at the two most adversarial corners. SEED=19. Double-SHA-256 self-gate.

What this does and does not show: M35 is itself NON-DISCRIMINATING (elasticity is shared by
both frameworks) -- so this is a METHOD demonstration: even a theory-laden [V] claim is
checked for input-dependence rather than trusted. The cascade's load-bearing VP-vs-mainstream
conclusions (the area-conservation identity dA_open+dA_close=0, and the dual-redox SIGN
argument) are DIMENSIONLESS / geometric and do not use density or thickness at all, so they
are contamination-proof by construction; this sweep targets the hardest remaining case.
"""
import hashlib, math

SEED = 19
G = 9.81
OBS = [("US_MidAtlantic", 300.0), ("North_Sea", 250.0)]

# pre-registered contamination ranges (literature spread), baseline in the middle
TE_KM = [40, 50, 60, 70, 80, 90, 100]
E_GPA = [50, 60, 70, 85, 100]
RHO_M = [3200, 3300, 3400]
NU    = [0.20, 0.25, 0.30]

EXPECT = "b32169721cbfb021f4b6ba9abfb2cd005c3ad8f3b877ed07238c19feee161a5f"


def alpha_km(E_Pa, Te_m, rho_m, nu):
    D = E_Pa * Te_m**3 / (12.0 * (1.0 - nu*nu))
    return ((4.0 * D / (rho_m * G)) ** 0.25) / 1e3


def holds(a_km):
    lo, hi = 0.6 * (0.5*math.pi*a_km), 1.4 * (1.0*math.pi*a_km)
    return all(lo <= off <= hi for _, off in OBS), (lo, hi)


def main():
    L = []
    L.append("INPUT-CONTAMINATION ROBUSTNESS SWEEP  (M35 forebulge; theory-laden geophysical inputs)")
    L.append(f"SEED={SEED}")
    L.append(f"observed forebulge offsets tested: {[o for _,o in OBS]} km")
    L.append("alpha ~ E^(1/4) * Te^(3/4) * rho_m^(-1/4) * (1-nu^2)^(-1/4)   (Te dominates)")
    L.append("")
    # baseline
    a0 = alpha_km(70e9, 70e3, 3300, 0.25)
    ok0, (lo0, hi0) = holds(a0)
    L.append(f"[BASELINE]  Te=70km E=70GPa rho_m=3300 nu=0.25")
    L.append(f"  alpha={a0:.1f} km ; widened band=[{lo0:.0f},{hi0:.0f}] km ; both bracketed={ok0}")
    L.append("")
    # full grid sweep
    total = 0; held = 0; amin = 1e9; amax = -1e9
    fail_examples = []
    for Te in TE_KM:
        for E in E_GPA:
            for rm in RHO_M:
                for nu in NU:
                    a = alpha_km(E*1e9, Te*1e3, rm, nu)
                    ok, _ = holds(a)
                    total += 1; held += 1 if ok else 0
                    amin = min(amin, a); amax = max(amax, a)
                    if not ok and len(fail_examples) < 4:
                        fail_examples.append((Te, E, rm, nu, a))
    L.append(f"[FULL-GRID SWEEP]  {len(TE_KM)}x{len(E_GPA)}x{len(RHO_M)}x{len(NU)} = {total} points")
    L.append(f"  alpha over the whole hypercube: [{amin:.1f}, {amax:.1f}] km")
    L.append(f"  grid points where BOTH observed offsets stay bracketed: {held}/{total}")
    if fail_examples:
        for Te, E, rm, nu, a in fail_examples:
            L.append(f"    FAIL: Te={Te} E={E} rho_m={rm} nu={nu} -> alpha={a:.1f}")
    L.append("")
    # exact Te survival window at the two most adversarial corners (fine scan)
    def survival_window(E, rm, nu):
        lo_edge = hi_edge = None
        Te = 5.0
        prev_ok = False
        while Te <= 400.0:
            a = alpha_km(E*1e9, Te*1e3, rm, nu)
            ok, _ = holds(a)
            if ok and lo_edge is None:
                lo_edge = Te
            if lo_edge is not None and not ok and hi_edge is None and Te > lo_edge:
                hi_edge = Te - 0.5
                break
            Te += 0.5
        if hi_edge is None and lo_edge is not None:
            hi_edge = 400.0
        return lo_edge, hi_edge
    # corner pushing alpha LOW (small E, high rho_m, low nu) and HIGH (big E, low rho_m, high nu)
    lo_corner = survival_window(min(E_GPA), max(RHO_M), min(NU))
    hi_corner = survival_window(max(E_GPA), min(RHO_M), max(NU))
    L.append("[Te SURVIVAL WINDOW]  (the offset-bracketing conclusion holds for Te in this range)")
    L.append(f"  at the alpha-LOW corner  (E={min(E_GPA)} rho_m={max(RHO_M)} nu={min(NU)}): Te in [{lo_corner[0]:.1f}, {lo_corner[1]:.1f}] km")
    L.append(f"  at the alpha-HIGH corner (E={max(E_GPA)} rho_m={min(RHO_M)} nu={max(NU)}): Te in [{hi_corner[0]:.1f}, {hi_corner[1]:.1f}] km")
    L.append(f"  => even at adversarial corners the conclusion needs only Te to lie roughly within")
    L.append(f"     [{max(lo_corner[0],hi_corner[0]):.0f}, {min(lo_corner[1],hi_corner[1]):.0f}] km;")
    L.append(f"     the plausible cratonic range [40,100] km sits INSIDE it.")
    L.append("")
    verdict = "ROBUST" if held == total else "INPUT-DEPENDENT"
    L.append("[VERDICT]")
    if held == total:
        L.append("  ROBUST: across the FULL contamination hypercube (all four theory-laden inputs")
        L.append("  simultaneously at every grid point including worst-case corners), both observed")
        L.append("  forebulge offsets stay bracketed. The conclusion does NOT depend on the precise")
        L.append("  (un-verifiable) values of Te / E / rho_m / nu. It would only break if Te fell")
        L.append("  below ~35 km or rose above ~160 km -- outside the literature range for the")
        L.append("  cratonic lithosphere these forebulges sit on. The theory-laden inputs are")
        L.append("  therefore NOT load-bearing here: auditing them to the bottom is unnecessary.")
    else:
        L.append("  INPUT-DEPENDENT: the conclusion flips somewhere inside the plausible ranges.")
        L.append("  The dependency is FLAGGED, not hidden; this input must be treated as load-bearing.")
    L.append("")
    L.append("  Scope: M35 is non-discriminating; this is a METHOD demonstration. The cascade's")
    L.append("  load-bearing VP-vs-mainstream claims (area-conservation identity; dual-redox sign)")
    L.append("  are dimensionless/geometric and do not use density or thickness at all -- robust by")
    L.append("  construction. Occurrence/ages stay [O]/RECORD, both directions.  Falsification = discovery.")

    body = "\n".join(L)
    print(body)
    print()
    dsha = hashlib.sha256(hashlib.sha256(body.encode("utf-8")).digest()).hexdigest()
    print(f"2xSHA256 = {dsha}")
    print(f"VERDICT_TOKEN = {verdict}")
    if EXPECT == "PLACEHOLDER":
        print("REPRO GATE: (EXPECT unset - pin this value)")
    else:
        assert dsha == EXPECT, f"LEDGER CHANGED: {dsha} != {EXPECT}"
        print("REPRO GATE: PASS")


if __name__ == "__main__":
    main()
