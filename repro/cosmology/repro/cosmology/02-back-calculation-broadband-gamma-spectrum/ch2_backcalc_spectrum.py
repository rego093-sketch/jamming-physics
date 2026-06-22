#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch2_backcalc_spectrum.py
========================
Vacuum-Inflow Cosmology · §2 (Light as the Lattice Elastic Wave) reproducibility.
repro/cosmology/02-light-lattice-elastic-wave-sharpest/ch2_backcalc_spectrum.py
VP_SPEC v1.8 · Constitution C3 (IRREPRODUCIBILITY_LEDGER, item B: gamma-ray
vacuum dispersion, [O] relaxed, not fully closed).

WHAT THIS SCRIPT ESTABLISHES (emission side)
--------------------------------------------
A single localized "shake" of the vacuum lattice is, by Fourier's theorem,
BROADBAND. Its short-wavelength (high-k) tail reaches the gamma band. A
calorimeter does not measure a wavelength; it measures the energy deposited by
the e+e- shower and *back-calculates* a photon energy. In the framework's own
optics the back-calculation is one map,

        E = hbar * omega = hbar * c * k                                   (1)

so the detector reports the high-k content of ONE disturbance as a spread of
photon energies. The famous "31 GeV photon" of GRB 090510 is then the ka ~ 0.1
component of one broadband shake (a ~63-cell wavelength, deep in the long-
wavelength / continuum regime) -- not an independent high-energy quantum that
must propagate as a discrete-lattice phonon.

The script makes this concrete: equal-energy sharp vs. smooth shakes; only the
SHARP one carries power into the GeV band, and the reach is fixed by the
disturbance's STRUCTURE (sharpness), not its amplitude.

WHAT THIS SCRIPT DOES *NOT* ESTABLISH (propagation side)
-------------------------------------------------------
It does NOT show that the gamma-band content arrives coherent with the low-
energy content over a cosmological baseline. That is the open dispersion item
(IRREPRODUCIBILITY_LEDGER B: [O] relaxed, not fully closed). Per the volume's
discipline, *exhibiting a broadband-emission mechanism is not deriving
dispersionless transport*. The collective-coherence question is treated by
ch2_gamma_collective.py and remains the one genuinely open dynamical item.

INVARIANTS
----------
* zero tuned constants: only hbar, c (CODATA) and the locked VP cell size
  a = 6.33e-19 m enter the physics. Pulse widths are arbitrary illustrative
  scales; the conclusion is shown width-independent (sweep below).
* determinism: SEED = 19; analytic pulses (no RNG path is taken); the canonical
  numeric digest is a 2x-SHA-256 over results rounded to 6 significant figures,
  so it is invariant across BLAS/FFT implementations.

Usage:
    python3 ch2_backcalc_spectrum.py            # numeric gate only
    python3 ch2_backcalc_spectrum.py --fig out.png   # also write the figure
"""

import sys
import json
import hashlib
import argparse

import numpy as np

# --------------------------------------------------------------------------- #
# Determinism seed (analytic pulses take no RNG path; set for SPEC compliance) #
# --------------------------------------------------------------------------- #
SEED = 19
np.random.seed(SEED)

# --------------------------------------------------------------------------- #
# Locked constants  (NOT tuned)                                               #
#   hbar, c : CODATA 2018 physical constants                                  #
#   a       : VP fundamental cell size, locked (IRREPRODUCIBILITY_LEDGER A;    #
#             two-length appendix C). The relevant lattice scale for light is  #
#             a, not the angular scale D = 4.8526 pm (§2, stiffness section).  #
# --------------------------------------------------------------------------- #
HBAR = 1.054571817e-34          # J s
C    = 2.99792458e8             # m s^-1
A    = 6.33e-19                 # m
EV   = 1.602176634e-19          # J / eV

# Energy <-> wavenumber map, Eq. (1), in lattice units (grid spacing = 1 cell):
#   kg = k * a  in rad/cell, range [0, pi];   E(kg) = (hbar c / a) * kg
E1_J  = HBAR * C / A            # photon energy at kg = 1 rad/cell
E1_EV = E1_J / EV

# --------------------------------------------------------------------------- #
# Lattice grid                                                                #
# --------------------------------------------------------------------------- #
N_LOG2 = 20
N      = 1 << N_LOG2            # 1,048,576 cells
X      = np.arange(N) - N // 2  # position in cells, centred


def gaussian_pulse(width_cells: float) -> np.ndarray:
    """A localized lattice displacement of given spatial width (in cells)."""
    g = np.exp(-0.5 * (X / float(width_cells)) ** 2)
    return g / np.sqrt(np.sum(g ** 2))   # normalize total energy -> isolate SHAPE


def energy_spectrum(field: np.ndarray):
    """Return (E_eV, kg, power) for a real field via rFFT and the Eq.(1) map."""
    F  = np.fft.rfft(field)
    f  = np.fft.rfftfreq(N, d=1.0)       # cycles/cell in [0, 0.5]
    kg = 2.0 * np.pi * f                 # rad/cell in [0, pi]
    P  = np.abs(F) ** 2
    E  = kg * E1_EV                      # eV
    return E, kg, P


def frac_above(E: np.ndarray, P: np.ndarray, E_thresh_eV: float) -> float:
    """Fraction of spectral power above an energy threshold."""
    return float(P[E >= E_thresh_eV].sum() / P.sum())


def sig(x: float, n: int = 6) -> float:
    """Round to n significant figures (digest stability across FFT backends)."""
    if x == 0.0:
        return 0.0
    from math import floor, log10
    return round(x, -int(floor(log10(abs(x)))) + (n - 1))


# --------------------------------------------------------------------------- #
# Computation                                                                 #
# --------------------------------------------------------------------------- #
def run():
    results = {
        "seed": SEED,
        "grid_log2": N_LOG2,
        "constants": {
            "hbar_Js": HBAR, "c_ms": C, "a_m": A,
            "E_at_ka1_GeV": sig(E1_EV / 1e9),
            "E_at_ka0p1_GeV": sig(0.1 * E1_EV / 1e9),     # the GRB 090510 photon
            "zone_edge_GeV": sig(np.pi * E1_EV / 1e9),
        },
    }

    # canonical sharp vs smooth (equal total energy)
    canon = {}
    for name, w in (("sharp_w2", 2.0), ("smooth_w5000", 5000.0)):
        E, _, P = energy_spectrum(gaussian_pulse(w))
        canon[name] = {
            "frac_above_1MeV":   sig(frac_above(E, P, 1e6)),
            "frac_above_100MeV": sig(frac_above(E, P, 1e8)),
            "frac_above_1GeV":   sig(frac_above(E, P, 1e9)),
        }
    results["canonical_pair"] = canon

    # width-independence sweep: does each shake reach the gamma (>1 GeV) band?
    # "reaches gamma" := non-negligible power above 1 GeV (fraction > 1e-3).
    sweep = {"sharp": {}, "smooth": {}}
    for w in (1.0, 2.0, 4.0):
        E, _, P = energy_spectrum(gaussian_pulse(w))
        sweep["sharp"][f"w{int(w)}"] = bool(frac_above(E, P, 1e9) > 1e-3)
    for w in (1000.0, 5000.0, 20000.0):
        E, _, P = energy_spectrum(gaussian_pulse(w))
        sweep["smooth"][f"w{int(w)}"] = bool(frac_above(E, P, 1e9) > 1e-3)
    results["reaches_gamma"] = sweep

    return results


# --------------------------------------------------------------------------- #
# Determinism gate: 2 x SHA-256 over the canonical (6-sig-fig) results         #
# --------------------------------------------------------------------------- #
def digest(results: dict) -> str:
    blob = json.dumps(results, sort_keys=True, separators=(",", ":")).encode("utf-8")
    h1 = hashlib.sha256(blob).digest()
    h2 = hashlib.sha256(h1).hexdigest()
    return h2


# --------------------------------------------------------------------------- #
# Figure (side artifact; NOT part of the gate)                                #
# --------------------------------------------------------------------------- #
def make_figure(path: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sharp  = gaussian_pulse(2.0)
    smooth = gaussian_pulse(5000.0)
    Es, _, Ps = energy_spectrum(sharp)
    Em, _, Pm = energy_spectrum(smooth)
    zone = np.pi * E1_EV

    fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(9, 8.5))

    win = 200
    sl = slice(N // 2 - win, N // 2 + win)
    ax0.plot(X[sl], sharp[sl] / sharp.max(),  color="#c0392b", lw=1.8,
             label="sharp 'churning' core (~2 cells)")
    ax0.plot(X[sl], smooth[sl] / smooth.max(), color="#2980b9", lw=1.8,
             label="smooth disturbance (~5000 cells)")
    ax0.set_xlabel("position  (lattice cells)")
    ax0.set_ylabel("lattice displacement (norm.)")
    ax0.set_title("A single localized shake of the vacuum lattice",
                  fontsize=12, fontweight="bold")
    ax0.legend(frameon=False, fontsize=9)
    ax0.grid(alpha=0.25)

    ms, mm = Es > 0, Em > 0
    ax1.loglog(Es[ms], Ps[ms] / Ps[ms].max(), color="#c0392b", lw=1.8,
               label="spectrum of the SHARP shake")
    ax1.loglog(Em[mm], Pm[mm] / Pm[mm].max(), color="#2980b9", lw=1.8,
               label="spectrum of the SMOOTH shake")
    ax1.axvspan(1e3, 1e6, color="#f1c40f", alpha=0.10)
    ax1.axvspan(1e6, 1e8, color="#e67e22", alpha=0.10)
    ax1.axvspan(1e8, zone, color="#e74c3c", alpha=0.10)
    for ee, nm in [(3e3, "keV\n(X-ray)"), (3e6, "MeV"), (3e9, "GeV\n(gamma)")]:
        ax1.text(ee, 1.4, nm, ha="center", va="bottom", fontsize=8, alpha=0.7)
    ax1.axvline(31e9, color="k", ls="--", lw=1.3)
    ax1.text(34e9, 1e-5, "GRB 090510\n31 GeV photon\n(ka=0.1, 63-cell λ)",
             fontsize=8.5, va="center")
    ax1.axvline(zone, color="gray", ls=":", lw=1.0)
    ax1.text(zone * 0.9, 1e-7, "lattice\nzone edge",
             fontsize=8, color="gray", va="center", ha="right")
    ax1.set_xlim(1e2, 3e12)
    ax1.set_ylim(1e-8, 2.5)
    ax1.set_xlabel("back-calculated photon energy  E = ħc·k   (eV)")
    ax1.set_ylabel("power spectral density (norm.)")
    ax1.set_title("Back-calculation: one shake → a broadband photon spectrum",
                  fontsize=12, fontweight="bold")
    ax1.legend(frameon=False, fontsize=9, loc="upper right")
    ax1.grid(alpha=0.25, which="both")

    plt.tight_layout()
    plt.savefig(path, dpi=140, bbox_inches="tight")
    return path


# --------------------------------------------------------------------------- #
# Main                                                                        #
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fig", metavar="PATH", default=None,
                    help="also write the figure to PATH (not gated)")
    args = ap.parse_args()

    results = run()
    d = digest(results)

    c = results["constants"]
    cp = results["canonical_pair"]
    print("ch2_backcalc_spectrum.py  —  §2 back-calculation / broadband-emission")
    print(f"[calibration] hbar*c/a = {c['E_at_ka1_GeV']:.1f} GeV  (E at ka = 1 rad/cell)")
    print(f"[check]       E(ka=0.1) = {c['E_at_ka0p1_GeV']:.2f} GeV"
          f"   <- GRB 090510 photon (ka~0.1, ~63-cell wavelength)")
    print(f"[check]       zone edge = {c['zone_edge_GeV']:.0f} GeV")
    print()
    print(f"[canonical]   SHARP  (w=2):    >1MeV={cp['sharp_w2']['frac_above_1MeV']:.3e}"
          f"  >100MeV={cp['sharp_w2']['frac_above_100MeV']:.3e}"
          f"  >1GeV={cp['sharp_w2']['frac_above_1GeV']:.3e}")
    print(f"[canonical]   SMOOTH (w=5000): >1MeV={cp['smooth_w5000']['frac_above_1MeV']:.3e}"
          f"  >100MeV={cp['smooth_w5000']['frac_above_100MeV']:.3e}"
          f"  >1GeV={cp['smooth_w5000']['frac_above_1GeV']:.3e}")
    print(f"[invariance]  reaches gamma (>1GeV)?  sharp={results['reaches_gamma']['sharp']}"
          f"  smooth={results['reaches_gamma']['smooth']}")
    print()
    print("[SCOPE] ESTABLISHED (emission): one localized lattice shake is broadband by")
    print("        construction; its high-k tail reaches the gamma band. '31 GeV' is the")
    print("        ka=0.1 component of one disturbance, not an independent quantum. Gamma")
    print("        reach is fixed by STRUCTURE (sharpness), not amplitude.")
    print("[SCOPE] NOT ESTABLISHED (propagation): coherence of the gamma-band content with")
    print("        the low-energy content over a cosmological baseline is NOT shown here.")
    print("        Open item [O] 'relaxed, not fully closed' (§2; LEDGER B). Exhibiting a")
    print("        broadband-emission mechanism is not deriving dispersionless transport.")
    print("[INVARIANT] zero tuned constants: only hbar, c (CODATA) and locked a enter the")
    print("        physics; pulse widths are arbitrary, conclusion is width-independent.")
    print()
    print(f"DETERMINISM-DIGEST (2xSHA-256, 6 sig-fig canonical): {d}")

    if args.fig:
        p = make_figure(args.fig)
        print(f"[figure] wrote {p}  (side artifact; not part of the gate)")

    return d


if __name__ == "__main__":
    main()
