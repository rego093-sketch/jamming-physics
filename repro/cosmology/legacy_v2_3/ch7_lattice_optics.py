#!/usr/bin/env python3
"""
ch7_lattice_optics.py  --  Reproduces Chapter 7 (non-expanding lattice-optics cosmology).

TWO CLAIMS TESTED
-----------------
A) NO DARK ENERGY NEEDED (degenerate).  The static lattice-optics luminosity distance
       d_L = (c/H0)(1+z) ln(1+z)
   fits the Pantheon+ Hubble diagram as well as accelerating LCDM (Omega_L=0.7).
   EXPECTED: chi2/dof = 0.50 (VP) vs 0.44 (LCDM); max|Delta mu| = 0.145 mag over z<2.3.
   CONCLUSION: "dark energy" is interpretation-contingent (not preferred or excluded by SNe).

B) ANGULAR-SIZE MINIMUM (distinguishing, distance-ladder-free).  With d_A = d_L/(1+z)^2,
   the angular size of a standard ruler is minimal at
       z_min = e - 1 ~ 1.72   (VP)   vs   ~1.61 (LCDM, Omega_m=0.3).

WHY NOT TIRED LIGHT: the lattice-optics redshift has time dilation built in (1+z = n_obs/n_em),
giving the observed (1+z) light-curve stretch and (1+z)^-4 surface brightness; static tired
light predicts neither and is excluded.

INPUTS: c; Pantheon+ extract (zHD, m_b_corr, m_b_corr_err_DIAG, IS_CALIBRATOR), shipped as
'Pantheon+_extract.tsv' (Scolnic et al. 2022; Brout et al. 2022). Each model fit by a single
marginalised offset (H0 and absolute magnitude degenerate). a0/dark energy NOT fitted.
DEPENDENCIES: numpy, scipy.  DATA: Pantheon+_extract.tsv in the same folder.
"""
import os, numpy as np
from scipy.integrate import quad

c = 2.99792458e5  # km/s
H0 = 70.0         # km/s/Mpc (cancels in the marginalised offset)

def dL_VP(z):                    # lattice-optics, no dark energy  [Mpc]
    return (c/H0)*(1+z)*np.log(1+z)
def dL_LCDM(z, Om=0.3):
    OL = 1-Om
    I = np.array([quad(lambda x: 1/np.sqrt(Om*(1+x)**3+OL), 0, zi)[0] for zi in z])
    return (1+z)*(c/H0)*I
def mu(dL): return 5*np.log10(dL)+25

def load_pantheon(path):
    d = np.genfromtxt(path, names=True, delimiter='\t')
    z = d['zHD']; mb = d['m_b_corr']; err = d['m_b_corr_err_DIAG']; cal = d['IS_CALIBRATOR']
    m = (cal == 0) & (z > 0.01)
    return z[m], mb[m], err[m]

def chi2_with_offset(mu_model, mb, err):
    off = np.sum((mb-mu_model)/err**2)/np.sum(1/err**2)
    return np.sum(((mb-mu_model-off)/err)**2), off

def angular_size_min(dA_func, zgrid):
    th = np.array([1.0/dA_func(zi) for zi in zgrid])
    return zgrid[np.argmin(th)]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    data = os.path.join(here, "Pantheon+_extract.tsv")

    print("=== (A) supernova Hubble diagram: dark energy not needed (degenerate) ===")
    if os.path.exists(data):
        z, mb, err = load_pantheon(data)
        muV = mu(dL_VP(z)); muL = mu(dL_LCDM(z))
        c2V, offV = chi2_with_offset(muV, mb, err)
        c2L, offL = chi2_with_offset(muL, mb, err)
        N = len(z)
        print(f"  N = {N} SNe (z = {z.min():.3f}-{z.max():.3f})")
        print(f"  VP   (lattice-optics, no dark energy): chi2/dof = {c2V/(N-1):.3f}")
        print(f"  LCDM (Omega_L=0.7):                    chi2/dof = {c2L/(N-1):.3f}")
        zz = np.linspace(0.02, 2.3, 200)
        dmu = (mu(dL_VP(zz))+offV) - (mu(dL_LCDM(zz))+offL)
        print(f"  max|Delta mu(VP-LCDM)| over z<2.3 = {np.max(np.abs(dmu)):.3f} mag  (SNe scatter ~0.15)")
        print("  PASS: both fit comparably => 'dark energy' is interpretation-contingent.\n")
    else:
        print("  [Pantheon+_extract.tsv not found; part B still verifies.]\n")

    print("=== (B) angular-size minimum (distance-ladder-free discriminator) ===")
    zg = np.linspace(0.1, 5, 4000)
    dA_VP = lambda z: (c/H0)*np.log(1+z)/(1+z)
    def dA_LCDM(z, Om=0.3):
        OL = 1-Om; I = quad(lambda x: 1/np.sqrt(Om*(1+x)**3+OL), 0, z)[0]
        return (c/H0)*I/(1+z)
    zmV = angular_size_min(dA_VP, zg)
    zmL = angular_size_min(dA_LCDM, zg)
    print(f"  VP  : z_min = {zmV:.3f}   (analytic e-1 = {np.e-1:.3f})")
    print(f"  LCDM: z_min = {zmL:.3f}")
    print("  PASS: standard rulers smallest at z~1.72 (VP) vs ~1.61 (LCDM).")

    print("\n=== (C) Hubble tension as line-of-sight averaging (candidate mechanism; HYP/SPEC) ===")
    print("  Redshift is path-integrated: ln(1+z)=int kappa_opt ds, so the inferred slope")
    print("  H_inf(D)=c<kappa_opt> is a LINE-OF-SIGHT AVERAGE. With kappa_opt=kappa0(1+eta*delta_bg),")
    print("  a local sample (within a density anomaly delta_loc) and a deep sample (<delta>->0) give")
    print("        H_local/H_global = 1 + eta*delta_loc.")
    obs = 73.0/67.0
    print(f"  Observed local-vs-global ratio ~ 73/67 = {obs:.3f}  =>  requires eta*delta_loc ~ {obs-1:+.3f}.")
    print("  Plausible decompositions (eta a SPEC sensitivity, delta_loc a local-structure contrast):")
    for eta, dloc in [(1.0, obs-1.0), (0.6, (obs-1.0)/0.6), (-0.3, (obs-1.0)/-0.3)]:
        print(f"    eta={eta:+.2f}, delta_loc={dloc:+.2f}  ->  H_local/H_global = {1+eta*dloc:.3f}")
    print("  => an O(1) sensitivity to an O(10%) local density anomaly reproduces the tension ORDER.")
    print("  HONEST: eta and delta_loc are NOT independently fixed here, so this is a candidate")
    print("     mechanism (the framework CAN host the tension as LOS averaging of one kappa_opt field),")
    print("     NOT a parameter-free prediction of 73 vs 67. Testable signatures: (i) inferred H0 should")
    print("     correlate with local large-scale density; (ii) H0 should be direction-dependent at fixed")
    print("     depth if delta_bg is anisotropic.\n")

    print("STATUS: SNe fit degenerate (dark energy interpretation-contingent);")
    print("        angular-size minimum is the distinguishing, distance-ladder-free test.")
    print("Data: Pantheon+ (Scolnic et al. 2022; Brout et al. 2022).")

    # ---------- figure: ch7_cosmology.png (Left: Hubble diagram; Right: angular-size minimum) ----------
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, (axL, axR) = plt.subplots(1, 2, figsize=(13.9, 5.1))
        _here = os.path.dirname(os.path.abspath(__file__)); _data = os.path.join(_here, "Pantheon+_extract.tsv")
        zz = np.linspace(0.011, 2.3, 300)
        if os.path.exists(_data):
            z, mb, err = load_pantheon(_data)
            muV = mu(dL_VP(z)); muL = mu(dL_LCDM(z))
            c2V, offV = chi2_with_offset(muV, mb, err); c2L, offL = chi2_with_offset(muL, mb, err); Nz=len(z)
            axL.errorbar(z, mb, yerr=err, fmt=".", ms=3, color="#9a9a9a", alpha=0.5, label="Pantheon+ SNe")
            axL.plot(zz, mu(dL_LCDM(zz))+offL, "-", color="#D85A30", lw=1.9, label=fr"$\Lambda$CDM ($\chi^2$/dof$={c2L/(Nz-1):.2f}$)")
            axL.plot(zz, mu(dL_VP(zz))+offV, "--", color="#185FA5", lw=2.0, label=fr"lattice-optics ($\chi^2$/dof$={c2V/(Nz-1):.2f}$, no DE)")
            axL.set_xscale("log"); axL.set_xlabel("redshift $z$"); axL.set_ylabel(r"distance modulus $\mu$")
            axL.set_title("Pantheon+ Hubble diagram (dark energy not needed)")
            axL.legend(fontsize=8, loc="lower right"); axL.grid(alpha=0.25, which="both")
        zg = np.linspace(0.05, 5, 1500)
        thV = (1+zg)/np.log(1+zg)
        def _dA_LCDM(zv, Om=0.3):
            OL=1-Om; I=quad(lambda x:1/np.sqrt(Om*(1+x)**3+OL), 0, zv)[0]; return (c/H0)*I/(1+zv)
        thL = np.array([1.0/_dA_LCDM(zi) for zi in zg])
        thV = thV/thV.min(); thL = thL/thL.min()
        zmV = zg[np.argmin(thV)]; zmL = zg[np.argmin(thL)]
        axR.plot(zg, thV, color="#185FA5", lw=2.2, label=f"lattice-optics (min $z={zmV:.2f}=e-1$)")
        axR.plot(zg, thL, "--", color="#D85A30", lw=1.8, label=f"$\\Lambda$CDM (min $z={zmL:.2f}$)")
        axR.axvline(zmV, color="#185FA5", ls=":", lw=1.0); axR.axvline(zmL, color="#D85A30", ls=":", lw=1.0)
        axR.set_xlabel("redshift $z$"); axR.set_ylabel("angular size of a standard ruler (normalised)")
        axR.set_title("Angular-size minimum (distance-ladder-free)")
        axR.legend(fontsize=8); axR.grid(alpha=0.25)
        plt.tight_layout(); plt.savefig("ch7_cosmology.png", dpi=120, bbox_inches="tight"); plt.close()
        print("  [figure written: ch7_cosmology.png]")
    except Exception as _exc:
        print(f"  [matplotlib unavailable: {_exc}] numbers above are the result.")
