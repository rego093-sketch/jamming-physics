#!/usr/bin/env python3
"""
ch7_sne.py  --  Chapter 7: the Pantheon+ supernova Hubble diagram, VP lattice-optics vs LCDM.

Re-implementation (2026-09-28) of a script cited on the site but lost. It supersedes part (A)
of legacy_v2_3/ch7_lattice_optics.py and follows that file's conventions (data file, cuts,
offset marginalisation), with numpy only.

CLAIM ON THE PAGES
------------------
  axh-provenance-ledger:  "Supernova chi2/dof=0.50 ... Pantheon+ (ch7_sne.py)"
  07-non-expanding-lattice-optics-cosmology: "the lattice-optics distance gives chi2/dof=0.50,
     against chi2/dof=0.44 for LCDM (Omega_L=0.7); the two distance laws differ by at most
     |Delta mu|=0.145 mag" and labels the fit "Degenerate ... fit ... equally well".

MODELS (each has exactly ONE free parameter: the additive offset M that absorbs H0 and the
SN absolute magnitude; nothing else is fitted)
  VP   : d_L = (c/H0) (1+z) ln(1+z)                       (static lattice optics, no dark energy)
  LCDM : d_L = (c/H0) (1+z) INT_0^z dz'/sqrt(Om(1+z')^3 + 1-Om),  Om = 0.3 FIXED (as on the page)
  mu = 5 log10(d_L/Mpc) + 25 + M

INPUTS (sources)
  ../legacy_v2_3/Pantheon+_extract.tsv : columns zHD, m_b_corr, m_b_corr_err_DIAG, IS_CALIBRATOR
      (Pantheon+; Scolnic et al. 2022, ApJ 938, 113; Brout et al. 2022, ApJ 938, 110).
  Cuts: IS_CALIBRATOR == 0 and zHD > 0.01  (same as the legacy script) -> N = 1580.
  Errors: DIAGONAL only (m_b_corr_err_DIAG). The full STAT+SYS covariance is not in the extract.
  c = 299792.458 km/s; H0 = 70 (cancels exactly in the marginalised offset).

ALGORITHM
  1. Offset M is marginalised ANALYTICALLY and IDENTICALLY for both models:
       chi2_min = A - B^2/C,  A = sum r^2/s^2, B = sum r/s^2, C = sum 1/s^2,  r = m_b - mu_0.
     (Full Gaussian marginalisation adds ln(C/2pi), which is the same number for both models
      because C depends only on the errors; so Delta chi2 is the same either way.)
  2. dof = N - 1 for both.  Delta chi2 = chi2_VP - chi2_LCDM (positive => LCDM preferred).
     With equal parameter counts, Delta AIC = Delta BIC = Delta chi2.
  3. Diagnostics: Delta chi2 contributions per redshift bin; Delta chi2 after rescaling the
     errors so the better model has chi2/dof = 1 (the diagonal errors are over-estimated for
     this purpose); max |Delta mu| over 0.02 < z < 2.3 after each model's best offset.
  4. Supplementary only (NOT the equal-parameter comparison): LCDM with Om free (2 params),
     via a deterministic grid.

EXPECTED OUTPUT (legacy run, same data): chi2/dof 0.499 (VP), 0.444 (LCDM); Delta chi2 ~ +87.

DETERMINISM: no RNG. Runtime < 5 s. DEPENDENCIES: numpy (matplotlib optional, MPLBACKEND=Agg).
"""
import os
import numpy as np

C_KMS = 299792.458
H0 = 70.0
OM_PAGE = 0.3

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "legacy_v2_3", "Pantheon+_extract.tsv")


def load_pantheon(path=DATA):
    d = np.genfromtxt(path, names=True, delimiter="\t")
    m = (d["IS_CALIBRATOR"] == 0) & (d["zHD"] > 0.01)
    return d["zHD"][m], d["m_b_corr"][m], d["m_b_corr_err_DIAG"][m]


def dL_VP(z):
    return (C_KMS / H0) * (1 + z) * np.log(1 + z)


def dL_LCDM(z, Om=OM_PAGE, zmax=3.0, n=60001):
    zg = np.linspace(0.0, zmax, n)
    f = 1.0 / np.sqrt(Om * (1 + zg) ** 3 + (1 - Om))
    I = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(zg))])
    return (C_KMS / H0) * (1 + z) * np.interp(z, zg, I)


def mu0(dL):
    return 5 * np.log10(dL) + 25


def chi2_marg(mu_model, mb, err):
    """Analytic minimisation over the additive offset (identical for every model)."""
    w = 1.0 / err ** 2
    r = mb - mu_model
    A, B, C = np.sum(w * r * r), np.sum(w * r), np.sum(w)
    off = B / C
    return A - B * B / C, off, (mb - mu_model - off) / err


if __name__ == "__main__":
    z, mb, err = load_pantheon()
    N = len(z)
    print("=== ch7_sne.py : Pantheon+ Hubble diagram, VP vs LCDM (same data, same free params) ===")
    print(f"  data: {os.path.relpath(DATA, HERE)}  N = {N} SNe, z = {z.min():.4f} .. {z.max():.3f}")
    print(f"  errors: diagonal (m_b_corr_err_DIAG); median sigma = {np.median(err):.3f} mag")

    c2V, offV, resV = chi2_marg(mu0(dL_VP(z)), mb, err)
    c2L, offL, resL = chi2_marg(mu0(dL_LCDM(z)), mb, err)
    dof = N - 1
    dchi2 = c2V - c2L
    print("\n--- (A) equal-parameter comparison: one marginalised offset each, dof = N-1 ---")
    print(f"  VP   (d_L=(c/H0)(1+z)ln(1+z))  : chi2 = {c2V:9.2f}   chi2/dof = {c2V/dof:.4f}   offset M = {offV:+.4f}")
    print(f"  LCDM (flat, Om=0.3 fixed)      : chi2 = {c2L:9.2f}   chi2/dof = {c2L/dof:.4f}   offset M = {offL:+.4f}")
    print(f"  Delta chi2 = chi2_VP - chi2_LCDM = {dchi2:+.2f}   (= Delta AIC = Delta BIC; equal k)")
    print(f"  likelihood ratio L_LCDM/L_VP = exp(Delta chi2/2) = 10^{dchi2/2/np.log(10):.1f}")
    print("  VERDICT: this is NOT degenerate. On the same data and the same number of free")
    print(f"           parameters, LCDM is preferred over VP by Delta chi2 = {dchi2:.1f} (diagonal errors).")

    # rescale errors so the better model has chi2/dof = 1 (diagonal errors are inflated)
    s = np.sqrt(min(c2V, c2L) / dof)
    print(f"\n--- (B) error-scale sensitivity ---")
    print(f"  both chi2/dof < 1 => diagonal errors are over-estimated (duplicate SNe from several")
    print(f"  surveys and the off-diagonal covariance are not modelled). Rescaling sigma by {s:.3f}")
    print(f"  so that the better model has chi2/dof = 1 gives Delta chi2 = {dchi2/s**2:+.1f}.")
    print("  (The full Pantheon+ covariance is needed for a final number; the diagonal value above")
    print("   is the conservative one.)")

    print("\n--- (C) where the Delta chi2 comes from (per-bin chi2_VP - chi2_LCDM, same offsets) ---")
    edges = [0.01, 0.03, 0.1, 0.3, 0.6, 1.0, 2.3]
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (z > lo) & (z <= hi)
        d = np.sum(resV[m] ** 2) - np.sum(resL[m] ** 2)
        mr = np.average(resV[m] * err[m] - resL[m] * err[m])
        print(f"  {lo:4.2f} < z <= {hi:4.2f}: n = {m.sum():4d}   dchi2 = {d:+7.2f}   mean(mu_VP - mu_LCDM) = {-mr:+.3f} mag")

    zz = np.linspace(0.02, 2.3, 400)
    dmu = (mu0(dL_VP(zz)) + offV) - (mu0(dL_LCDM(zz)) + offL)
    print(f"\n--- (D) max|Delta mu(VP - LCDM)| over 0.02 < z < 2.3 (best offsets) = {np.max(np.abs(dmu)):.3f} mag")

    print("\n--- (E) supplementary (NOT equal-parameter): LCDM with Om free on a grid ---")
    oms = np.round(np.arange(0.05, 0.701, 0.005), 3)
    c2s = np.array([chi2_marg(mu0(dL_LCDM(z, Om=o)), mb, err)[0] for o in oms])
    ib = int(np.argmin(c2s))
    print(f"  best Om = {oms[ib]:.3f}, chi2 = {c2s[ib]:.2f} (dof = {N-2});  "
          f"Delta chi2(VP - LCDM_free) = {c2V - c2s[ib]:+.2f}, Delta AIC = {c2V - c2s[ib] - 2:+.2f}")

    print("\nPAGE CLAIM  chi2/dof = 0.50 (VP) vs 0.44 (LCDM): numbers REPRODUCED "
          f"({c2V/dof:.3f} vs {c2L/dof:.3f}).")
    print("PAGE LABEL  'degenerate / fit equally well': NOT SUPPORTED. "
          f"Delta chi2 = {dchi2:+.1f} for {N} SNe with equal parameters.")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.5, 7), sharex=True,
                                     gridspec_kw={"height_ratios": [2, 1]})
        order = np.argsort(z)
        a1.errorbar(z, mb, yerr=err, fmt=".", ms=2, color="#999999", alpha=0.4, label="Pantheon+")
        a1.plot(zz, mu0(dL_LCDM(zz)) + offL, color="#D85A30", label=f"LCDM Om=0.3 (chi2={c2L:.0f})")
        a1.plot(zz, mu0(dL_VP(zz)) + offV, "--", color="#185FA5", label=f"VP (chi2={c2V:.0f})")
        a1.set_xscale("log"); a1.set_ylabel("m_b_corr"); a1.legend(fontsize=8)
        a2.plot(zz, dmu, color="#185FA5"); a2.axhline(0, color="k", lw=0.6)
        a2.set_ylabel("mu_VP - mu_LCDM"); a2.set_xlabel("z")
        a1.set_title(f"Delta chi2 (VP - LCDM) = {dchi2:+.1f}, equal parameters")
        plt.tight_layout()
        plt.savefig(os.path.join(HERE, "ch7_sne.png"), dpi=110)
        print("  [figure written: ch7_sne.png]")
    except Exception as exc:
        print(f"  [matplotlib unavailable: {exc}] numbers above are the result.")
