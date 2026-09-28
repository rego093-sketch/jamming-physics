#!/usr/bin/env python3
"""
ch12_sunspot.py -- Sunspot as an inflow-driven converging/downdraft SINK (VP inflow dynamics).

STATUS: HYP/SPEC, illustrative toy. It shows the OBSERVED sunspot phenomenology is consistent
with a central inflow-sink, and is DEGENERATE with standard magnetoconvection (same observables).
The distinguishing claim is the causal order: VP says the converging INFLOW is primary and
ORGANIZES the field; the dynamo says the field is primary. Not a first-principles derivation.

Observations targeted (sources in the chapter text):
  - downflow + converging horizontal inflow beneath the spot (Duvall et al. 1996)  <-- the toy's core
  - Wilson depression ~400-800 km (tau=1 surface sunk)
  - strong vertical umbral field ~3 kG; umbra T~3800 K (dark)
  - surface return outflows (Evershed/moat) -- a SEPARATE, debated shallow component (not in the toy)

TOY PIECES:
  (1) converging-inflow + downdraft flow toward a subsurface sink (the Duvall picture)
  (2) flux freezing: a converging inflow concentrates the vertical field 100 G -> ~3 kG
  (3) cooling from suppressed vertical heat throughput: T^4 with ~82% blocked -> ~3800 K
  (4) Wilson depression order-of-magnitude from the magnetic-pressure deficit
DEPENDENCIES: numpy, matplotlib.
"""
import numpy as np

def sink_flow(R=1.0, D=1.0, d_sink=0.45, nr=44, nz=40):
    """Potential flow toward a subsurface line/point sink at (r=0, z=-d_sink), with an image
    sink at z=+d_sink so the surface z=0 is (approximately) a streamline. Returns the velocity
    field -> converging horizontal inflow + central downdraft (the observed Duvall picture)."""
    r = np.linspace(0.02, R, nr); z = np.linspace(-D, -0.02, nz)
    Rg, Zg = np.meshgrid(r, z)
    def vel(zc):                      # flow toward a sink at (0, zc): u ~ -(x-xs)/|..|^3
        dz = Zg - zc; dist2 = Rg**2 + dz**2
        ur = -Rg/dist2**1.5; uz = -dz/dist2**1.5
        return ur, uz
    ur1, uz1 = vel(-d_sink)           # real sink (below surface)
    ur2, uz2 = vel(+d_sink)           # image sink (above surface) -> surface ~ streamline
    ur = ur1 + ur2; uz = uz1 + uz2
    return r, z, Rg, Zg, ur, uz

def field_concentration(Bz_quiet_G=100.0, conv_ratio=30.0):
    return Bz_quiet_G, Bz_quiet_G*conv_ratio             # Gauss (area-convergence factor)

def Bz_profile(R=1.0, r_core=0.18, Bz_quiet_G=100.0, Bz_umbra_G=3000.0, n=400):
    r = np.linspace(0, R, n)
    return r, Bz_quiet_G + (Bz_umbra_G-Bz_quiet_G)*np.exp(-(r/r_core)**2)

def cooling(Tphot=5800.0, blocked=0.82):
    return Tphot*(1-blocked)**0.25                       # F~T^4

def wilson_depression(B=0.3, Pgas=1.4e4, H=250e3):
    mu0=4*np.pi*1e-7; Pmag=B**2/(2*mu0)
    return Pmag, H*np.log((Pgas+Pmag)/Pgas)              # tau=1 surface sinks ~ a few scale heights

if __name__ == "__main__":
    print("=== Sunspot as an inflow-driven converging/downdraft SINK (HYP/SPEC, illustrative) ===\n")

    print("(1) flow toward a subsurface sink => converging horizontal inflow + central downdraft")
    r,z,Rg,Zg,ur,uz = sink_flow()
    i_out = int(0.4*len(r)); above = z > -0.45     # region between the surface and the sink
    print(f"    near-surface mean u_r = {np.mean(ur[-1, i_out:]):+.2f}  (CONVERGING inflow, sign -)")
    print(f"    above-sink core mean u_z = {np.mean(uz[above][:, :int(0.15*len(r))]):+.2f}  (DOWNDRAFT, sign -)")
    print("    => matches Duvall et al. 1996 (downflow + near-surface inflow beneath the spot).")
    print("    NOTE: the shallow surface OUTFLOWS (Evershed/moat) are a separate component, not in this toy.\n")

    print("(2) flux freezing: a converging inflow concentrates the vertical field")
    bq, bu = field_concentration()
    print(f"    Bz: {bq:.0f} G (quiet) x area-convergence 30 -> {bu:.0f} G = {bu/1000:.1f} kG (umbra ~3 kG).\n")

    print("(3) cooling: the concentrated field/downdraft suppresses the vertical heat throughput")
    print(f"    ~82% of the convective heat flux blocked -> T = 5800*(0.18)^0.25 = {cooling():.0f} K (umbra ~3800 K).\n")

    print("(4) Wilson depression: the magnetic-pressure deficit sinks the tau=1 surface")
    Pmag, depth = wilson_depression()
    print(f"    P_mag(B=0.3T) = {Pmag:.2e} Pa (>~ photospheric gas pressure); tau=1 surface sinks")
    print(f"    ~ a few pressure scale heights ~ {depth/1e3:.0f} km -- same order as observed ~400-800 km.\n")

    print("HONEST: HYP/SPEC; same observables as standard magnetoconvection (degenerate). The toy")
    print("shows inflow-dynamics CONSISTENCY, not superiority. Distinguishing claim = causal order")
    print("(inflow organizes the field vs field-first dynamo); the observed flux-emergence-then-")
    print("converging-flow sequence is the key tension/test for the inflow-primary reading.")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig,(a1,a2)=plt.subplots(1,2,figsize=(11,4.3))
        spd = np.sqrt(ur**2+uz**2)
        a1.streamplot(Rg, Zg, ur, uz, density=1.1, color="#185FA5", linewidth=0.8, arrowsize=0.9)
        a1.plot(0,-0.45,"o",color="#D85A30",ms=7); a1.text(0.05,-0.45,"sink (downdraft)",color="#D85A30",fontsize=9)
        a1.set_xlim(0,1); a1.set_ylim(-1,0); a1.set_xlabel("r / R"); a1.set_ylabel("z (depth)")
        a1.set_title("converging inflow + downdraft (Duvall 1996)")
        rr, prof = Bz_profile()
        a2.plot(rr, prof, color="#D85A30", lw=2)
        a2.axhline(3000, ls=":", color="#888780"); a2.text(0.5,3120,"umbra ~3 kG",fontsize=8,color="#888780")
        a2.set_ylim(0,3500); a2.set_xlabel("r / R"); a2.set_ylabel("$B_z$ (G)")
        a2.set_title("field concentrated by the converging inflow (flux freezing)")
        plt.tight_layout(); plt.savefig("ch12_sunspot.png", dpi=110, bbox_inches="tight")
        print("\n[figure written: ch12_sunspot.png]")
    except Exception as e:
        print(f"[matplotlib unavailable: {e}]")
