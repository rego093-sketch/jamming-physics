#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_cap_depart.py
VP Theory — G-CAP-DEPART: where (and whether) the cap makes VP gravity DEPART from Schwarzschild,
confronted with neutron-star (PSR J0740+6620) and black-hole ringdown (GWTC-3/GW250114) data.

This is an ADVERSARIAL test: the framework reproduces GR by design, so it can only be TESTED where
it DEPARTS. We locate the cap fluidization radius as a framework quantity, trace it through the
framework's OWN two-channel structure (App G: g_geom far-field vs g_restore contact), and tabulate
whether the implied departure is observable / excluded.

Framework inputs (referenced):
  - river identity: gravitational time dilation = sqrt(1 - v_river^2/c^2) = sqrt(1 - 2GM/rc^2)
    EXACTLY, where v_river(r) = sqrt(2GM/r), wherever the medium is JAMMED (G-RIVER, proven).
  - cap (sec 17.4.2): inflow saturates; the medium unjams/FLUIDIZES when the inflow velocity reaches
    a yield fraction alpha of the signal speed c:  v_river(r) = alpha * c.  => r_fluid = r_s / alpha^2.
    alpha is the framework's [O] yield-velocity fraction (Psi_yield class). alpha=1 = sonic (most forced).
  - two channels (App G): g_geom (curvature, far-field: redshift/orbits/light/GW) is UNCAPPED = GR;
    g_restore (contact normal force) is capped at g_* and only affects contact mechanics.

Empirical anchors (web-sourced 2024-2025):
  - PSR J0740+6620: M = 2.08 Msun, R = 12.92 km (NICER). Pulse profile GR-consistent.
  - BH ringdown light ring ~1.5 r_s: QNM fractional deviation |eps_Omega| < 0.05 (GWTC-3); GR-consistent.

Deterministic, standard-library only (math). 2x sha256 identical.
"""

import math
import hashlib
import io
import csv

GM_SUN_OVER_C2_KM = 1.476625   # km  (= G*Msun/c^2); r_s(M) = 2 * this * (M/Msun)

# Compact objects: name -> (M[Msun], R[km] or None for BH-defined radii)
def r_s_km(M_sun):
    return 2.0 * GM_SUN_OVER_C2_KM * M_sun

def v_river_over_c(r_over_rs):
    """v_river/c = sqrt(r_s/r) = sqrt(1 / (r/r_s))."""
    return math.sqrt(1.0 / r_over_rs)

def z_gr(r_over_rs):
    """GR gravitational redshift at r = (r_over_rs) * r_s:  z = 1/sqrt(1 - r_s/r) - 1."""
    return 1.0 / math.sqrt(1.0 - 1.0 / r_over_rs) - 1.0

def z_vp_geom(r_over_rs):
    """VP redshift in the geom/river channel = sqrt(1 - v_river^2/c^2)^-1 - 1 = EXACT GR (river identity)."""
    v = v_river_over_c(r_over_rs)
    return 1.0 / math.sqrt(1.0 - v * v) - 1.0

# ---- objects / probed radii (in units of their own r_s) ----
NS = {
    "PSR J0740 (2.08Msun,12.92km)": (2.08, 12.92),
    "fiducial NS (1.4Msun,12km)":   (1.40, 12.00),
}
BH_RADII = {   # characteristic radii probed by GW observations, in units of r_s
    "ISCO (3 r_s)":       3.0,
    "light ring (1.5 r_s)": 1.5,
    "horizon (1 r_s)":    1.0,
}

def ns_rows():
    rows = []
    for name, (M, R) in NS.items():
        rs = r_s_km(M)
        ror = R / rs
        rows.append((name, M, R, rs, ror, v_river_over_c(ror), z_gr(ror), z_vp_geom(ror),
                     math.sqrt(1.0 / ror)))  # alpha_min to keep this surface jammed = v_river/c
    return rows

def bh_rows():
    rows = []
    for name, ror in BH_RADII.items():
        vr = v_river_over_c(ror)
        amin = vr  # alpha_min so that r_fluid = r_s/alpha^2 <= this radius
        rows.append((name, ror, vr, amin))
    return rows

def alpha_grid_rows():
    rows = []
    for alpha in (0.30, 0.50, 0.587, 0.69, 0.75, 0.816, 0.90, 0.99, 1.00):
        rfl = 1.0 / alpha**2  # r_fluid / r_s
        # is each probe radius fluidized (departed) ?  fluidized if r_probe <= r_fluid
        ns_surf_J0740 = 12.92 / r_s_km(2.08)          # ~2.103
        ns_surf_fid = 12.00 / r_s_km(1.40)            # ~2.902
        flags = {
            "NS J0740 surf(2.10)": "DEPART" if ns_surf_J0740 <= rfl else "GR-exact",
            "NS fid surf(2.90)":   "DEPART" if ns_surf_fid <= rfl else "GR-exact",
            "ISCO(3.0)":           "DEPART" if 3.0 <= rfl else "GR-exact",
            "lightring(1.5)":      "DEPART" if 1.5 <= rfl else "GR-exact",
        }
        rows.append((alpha, rfl, flags))
    return rows

def build_csv():
    buf = io.StringIO(); w = csv.writer(buf, lineterminator="\n")
    w.writerow(["# VP G-CAP-DEPART confrontation (deterministic)"])
    w.writerow(["# r_fluid/r_s = 1/alpha^2 ; alpha = yield-velocity fraction (framework [O]); alpha=1 sonic"])
    w.writerow([])
    w.writerow(["# Compact objects: surface inflow and redshift (geom/river channel)"])
    w.writerow(["object", "M_Msun", "R_km", "r_s_km", "R/r_s", "v_river/c@surf",
                "z_GR", "z_VP_geom", "z_VP-z_GR", "alpha_min_to_stay_jammed"])
    for (name, M, R, rs, ror, vr, zg, zv, amin) in ns_rows():
        w.writerow([name, "%.2f" % M, "%.2f" % R, "%.3f" % rs, "%.3f" % ror, "%.4f" % vr,
                    "%.4f" % zg, "%.4f" % zv, "%.2e" % (zv - zg), "%.3f" % amin])
    w.writerow([])
    w.writerow(["# BH characteristic radii probed by GW (in r_s)"])
    w.writerow(["radius", "r/r_s", "v_river/c", "alpha_min_to_stay_jammed"])
    for (name, ror, vr, amin) in bh_rows():
        w.writerow([name, "%.2f" % ror, "%.4f" % vr, "%.3f" % amin])
    w.writerow([])
    w.writerow(["# alpha grid: r_fluid/r_s and which probes are fluidized (DEPART) vs GR-exact"])
    w.writerow(["alpha", "r_fluid/r_s", "NS_J0740(2.10)", "NS_fid(2.90)", "ISCO(3.0)", "lightring(1.5)"])
    for (alpha, rfl, flags) in alpha_grid_rows():
        w.writerow(["%.3f" % alpha, "%.3f" % rfl,
                    flags["NS J0740 surf(2.10)"], flags["NS fid surf(2.90)"],
                    flags["ISCO(3.0)"], flags["lightring(1.5)"]])
    return buf.getvalue()

def selftest():
    # river identity: VP geom redshift == GR redshift to machine precision, all radii
    for ror in (1.5, 2.0, 2.103, 2.902, 3.0, 10.0):
        assert abs(z_vp_geom(ror) - z_gr(ror)) < 1e-12, "river identity broken at r/r_s=%.3f" % ror
    # PSR J0740 surface numbers
    rs = r_s_km(2.08)
    assert abs(rs - 6.143) < 0.01, "r_s(2.08) wrong: %.3f" % rs
    ror = 12.92 / rs
    assert abs(v_river_over_c(ror) - 0.6896) < 1e-3, "J0740 surf v_river/c wrong"
    assert abs(z_gr(ror) - 0.3808) < 1e-3, "J0740 z_GR wrong: %.4f" % z_gr(ror)
    # exclusion logic: alpha_min(light ring) = sqrt(1/1.5)
    assert abs(math.sqrt(1.0/1.5) - 0.8165) < 1e-3, "light-ring alpha_min wrong"
    # sonic alpha=1 => r_fluid = r_s (horizon): no probe radius > r_s is fluidized
    rfl = 1.0/1.0**2
    assert rfl == 1.0, "sonic r_fluid != r_s"
    assert 2.103 > rfl and 1.5 > rfl, "sonic case should leave NS surf and light ring GR-exact"
    return True

def main():
    assert selftest(), "selftest failed"
    csv_text = build_csv()
    h1 = hashlib.sha256(csv_text.encode()).hexdigest()
    h2 = hashlib.sha256(build_csv().encode()).hexdigest()
    assert h1 == h2, "non-deterministic"
    with open("CAP_DEPART_LEDGER.csv", "w", encoding="utf-8") as fh:
        fh.write(csv_text)

    print("=" * 86)
    print("VP G-CAP-DEPART  —  does the cap make VP gravity depart from Schwarzschild? (vs NS / ringdown)")
    print("=" * 86)
    print("Cap fluidization radius (framework): r_fluid = r_s / alpha^2,  alpha = yield-velocity fraction")
    print("  (alpha=1 = sonic, the most-forced value, since c is the medium's max signal speed).")
    print()
    print("[1] Surface inflow & redshift (geom/river channel = EXACT GR by the river identity):")
    print("  %-32s %-8s %-9s %-9s %-9s %-12s" %
          ("object", "R/r_s", "v_riv/c", "z_GR", "z_VP", "z_VP - z_GR"))
    for (name, M, R, rs, ror, vr, zg, zv, amin) in ns_rows():
        print("  %-32s %-8.3f %-9.4f %-9.4f %-9.4f %-12.1e" % (name, ror, vr, zg, zv, zv - zg))
    print("  => VP redshift == GR redshift to machine precision: the river/geom channel CANNOT depart")
    print("     (it is exact Schwarzschild). NICER's GR-based pulse fit of PSR J0740 is auto-consistent.")
    print()
    print("[2] BH radii probed by GW, and alpha needed to keep them JAMMED (no departure):")
    for (name, ror, vr, amin) in bh_rows():
        print("  %-22s r/r_s=%.2f   v_river/c=%.4f   needs alpha > %.3f" % (name, ror, vr, amin))
    print()
    print("[3] For each yield fraction alpha: r_fluid/r_s and which probes FLUIDIZE (could depart):")
    print("  %-7s %-12s %-14s %-13s %-10s %-12s" %
          ("alpha", "r_fluid/r_s", "NS_J0740(2.10)", "NS_fid(2.90)", "ISCO(3.0)", "lightring(1.5)"))
    for (alpha, rfl, flags) in alpha_grid_rows():
        print("  %-7.3f %-12.3f %-14s %-13s %-10s %-12s" %
              (alpha, rfl, flags["NS J0740 surf(2.10)"], flags["NS fid surf(2.90)"],
               flags["ISCO(3.0)"], flags["lightring(1.5)"]))
    print()
    print("VERDICT (honest, layered):")
    print("  (L1) Most-forced reading alpha=1 (sonic): r_fluid = r_s = HORIZON. Every observable radius")
    print("       is OUTSIDE => VP = exact Schwarzschild everywhere accessible. Moreover the cap (g_restore)")
    print("       is a CONTACT normal-force effect (App G); redshift/orbits/light/GW are the UNCAPPED geom")
    print("       channel = GR. => G-CAP-DEPART is OBSERVATIONALLY NULL in all clean channels. The gravity")
    print("       sector is DEGENERATE with GR: it cannot be tested or excluded this way.")
    print("  (L2) Earlier-yield readings alpha<1 (river breaks before sonic) would depart at r_fluid>r_s:")
    print("       - alpha < 0.690 => departs at/above PSR J0740 surface => EXCLUDED (GR-consistent NICER fit).")
    print("       - alpha < 0.816 => departs at/above the BH light ring => in tension with ringdown")
    print("         (|eps_Omega|<0.05) IF ringdown probes the affected channel.")
    print("       Survival requires alpha >~ 0.82 (near-sonic yield).")
    print("  (L3) TENSION: the framework's own medium jams at the ISOSTATIC, MARGINALLY-rigid point")
    print("       (z=6, phi_jam~0.64). Marginal rigidity argues for EARLY yield (small alpha) -> excluded.")
    print("       Survival (alpha>~0.82, near-sonic rigidity) conflicts with marginal-isostatic jamming.")
    print()
    print("  BOTTOM LINE: the cap/gravity sector yields NO surviving prediction distinct from GR in")
    print("  accessible regimes -- it is either degenerate (alpha=1) or excluded (alpha<0.82, which the")
    print("  framework's own jamming favors). The theory's empirical testability therefore rests on the")
    print("  OTHER channel: cosmological (1+z) time dilation (still open). [honest negative result]")
    print()
    print("No-Tuning: no coefficient migrated. ledger sha256 = %s" % h1)
    print("wrote: CAP_DEPART_LEDGER.csv")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
