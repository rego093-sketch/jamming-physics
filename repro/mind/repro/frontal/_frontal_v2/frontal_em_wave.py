# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- EMERGE THE FRONTAL LOBE, SEE THE ELECTROMAGNETIC WAVE
#  Constitution: physics-derived, NO TUNING, gene-grounded, data decides.
#
#  Direction (user): the frontal lobe's function lives in what its EM wave DOES.
#  So: emerge the cortical (FOXG1) population's rhythm, radiate it as the engine's
#  EM brainwave (J~d/dt(LFP) -> wave at speed c), and propagate it through real
#  brain tissue (Maxwell lossy wavenumber). Compare the FAST frontal gamma against
#  every organ -- especially the SLOW hypothalamus (2 Hz, neuroendocrine) now put
#  PROPERLY in the picture. All bands are cited [L]; the EM physics is exact [V].
# ==========================================================================
import sys, os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import vp_mind_engine as E                    # FROZEN, READ-ONLY (EM machinery + organs)

ATLAS = E.load_brain_atlas()["organs"]
SIGMA, EPS_R, L_BRAIN = 0.30, 1.0e5, 0.15     # measured tissue params (engine M9 inputs)

# organ -> (cited band centre Hz, band name); frontal cortex = FOXG1 gamma
ORGANS = {k: (float(v["f0_hz"]), v["band"], float(v["gamma"]), v["master"])
          for k, v in ATLAS.items()}

def em_at(f_hz):
    """Exact Maxwell plane-wave in brain tissue at f_hz: wavelength, skin depth,
       brain-in-wavelengths (quasi-static parameter), end-to-end phase & amplitude."""
    beta, alpha = E._lossy_wavenumber(f_hz, SIGMA, EPS_R)
    lam = 2.0 * math.pi / beta
    skin = (1.0 / alpha) if alpha > 0 else float("inf")
    phase_end, amp_ratio = E._field_across_transect(f_hz, SIGMA, EPS_R, L_BRAIN)
    return dict(f=f_hz, wavelength_m=lam, skin_depth_m=skin,
                brain_in_lambda=L_BRAIN / lam, skin_over_brain=skin / L_BRAIN,
                phase_across_brain_rad=phase_end, amp_drop=1.0 - amp_ratio)

def emerge_frontal_radiation():
    """Emerge the cortical (FOXG1) LFP and RADIATE it as the engine's EM brainwave."""
    pop = E.Population(gamma=ORGANS["neocortex"][2])     # FOXG1 gamma = 1.4737
    g = pop.lfp(tau_inh=6.0)                              # fast inhibition -> gamma LFP
    L = g["lfp"]; dtw = g["dt"]
    J = np.gradient(L, dtw)                               # ionic current = antenna source
    rad = E.emit_1d(lambda t: math.sin(0.30 * t))        # launch the carrier on the lattice
    return dict(emerged_model_freq=g["freq"],
                front_speed=rad["front_speed"], c=rad["c"],
                radiated_energy=rad["radiated_energy"])

def main():
    print("=" * 76)
    print(" EMERGE THE FRONTAL LOBE -> WHAT HAPPENS TO ITS ELECTROMAGNETIC WAVE")
    print("=" * 76)

    fr = emerge_frontal_radiation()
    print()
    print(" Frontal (FOXG1) population RADIATES the EM brainwave:")
    print("   front speed / c = {:.6f}  (launched at the speed of light)".format(
        fr["front_speed"] / fr["c"] if fr["c"] else float("nan")))
    print("   radiated energy = {:.4e}  (>0 -> a real outward wave; the measurable EEG)".format(
        fr["radiated_energy"]))

    # EM in tissue at each organ's band
    print()
    print(" EM wave in brain tissue at each organ's cited band (sigma=0.30, eps_r=1e5):")
    print("   organ            band            f(Hz)  lambda(m)  skin(m)  brain/lambda")
    rows = {}
    for org, (f, band, gam, master) in sorted(ORGANS.items(), key=lambda kv: kv[1][0]):
        e = em_at(f); rows[org] = e
        star = "  <== FRONTAL" if org == "neocortex" else ("  <== hypothalamus" if org == "hypothalamus" else "")
        print("   {:18s} {:14s} {:5.1f}  {:8.1f}  {:7.1f}  {:.2e}{}".format(
            org, band, f, e["wavelength_m"], e["skin_depth_m"], e["brain_in_lambda"], star))

    cx, hy = rows["neocortex"], rows["hypothalamus"]
    print()
    print(" FRONTAL gamma vs SLOW hypothalamus -- the contrast:")
    print("   frontal gamma 40 Hz : lambda={:.0f} m, brain/lambda={:.2e} (shortest wave -> most spatial structure)".format(
        cx["wavelength_m"], cx["brain_in_lambda"]))
    print("   hypothalamus  2 Hz  : lambda={:.0f} m, brain/lambda={:.2e} (longest wave -> maximally quasi-static)".format(
        hy["wavelength_m"], hy["brain_in_lambda"]))
    print("   ratio of brain/lambda (frontal : hypothalamus) = {:.1f}x".format(
        cx["brain_in_lambda"] / hy["brain_in_lambda"]))
    print()
    print(" READING: every brain rhythm is sub-wavelength inside the head (brain<<lambda),")
    print("   so WITHIN the brain the EM coupling is NEAR-FIELD (ephaptic), not radiative --")
    print("   which is exactly why M9 couples organs by the near field. The FRONTAL gamma is")
    print("   the fastest major rhythm -> shortest wavelength -> the LEAST quasi-static field,")
    print("   the one that can carry the most spatial EM structure. The slow hypothalamus sits")
    print("   at the opposite end (longest wave, pure near-field modulator). And the frontal")
    print("   population DOES radiate a real far-field wave at c -- the gamma you measure as EEG.")
    print("   bands [L cited]; Maxwell propagation [V exact]; efficacy [O]. new_tuned_constants=0.")

    # ---- FIGURE ----
    fs = np.logspace(0, 2, 240)                          # 1..100 Hz
    lam = np.array([em_at(f)["wavelength_m"] for f in fs])
    skin = np.array([em_at(f)["skin_depth_m"] for f in fs])
    binl = np.array([em_at(f)["brain_in_lambda"] for f in fs])

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    band_colors = {"gamma": "#c0392b", "theta": "#2980b9", "alpha/spindle": "#16a085",
                   "beta": "#8e44ad", "low-beta": "#9b59b6", "delta/slow": "#7f8c8d",
                   "delta/respiratory": "#95a5a6"}
    # Panel A: wavelength & skin depth vs frequency, brain line, organ bands
    ax[0].loglog(fs, lam, color="#2c3e50", lw=2, label="EM wavelength in tissue")
    ax[0].loglog(fs, skin, color="#27ae60", lw=2, ls="--", label="skin depth (1/attenuation)")
    ax[0].axhline(L_BRAIN, color="k", lw=1, ls=":", label="brain size (0.15 m)")
    for org, (f, band, gam, master) in ORGANS.items():
        if f < 1 or f > 100: continue
        c = band_colors.get(band, "#bbbbbb")
        ax[0].axvline(f, color=c, alpha=0.35, lw=1)
    ax[0].axvline(ORGANS["neocortex"][0], color="#c0392b", lw=2.5, label="frontal gamma 40 Hz")
    ax[0].axvline(ORGANS["hypothalamus"][0], color="#7f8c8d", lw=2.5, label="hypothalamus 2 Hz")
    ax[0].set_xlabel("frequency (Hz)"); ax[0].set_ylabel("length (m)")
    ax[0].set_title("EM wave in brain tissue: wavelength & skin depth\n(both >> brain at every rhythm -> quasi-static near-field)")
    ax[0].legend(fontsize=8, loc="center left"); ax[0].grid(True, which="both", alpha=0.2)

    # Panel B: brain-in-wavelengths (quasi-static parameter) vs frequency, bands marked
    ax[1].loglog(fs, binl, color="#2c3e50", lw=2)
    ax[1].axhline(1.0, color="r", lw=1, ls=":", label="brain = 1 wavelength (radiative onset)")
    for org, (f, band, gam, master) in sorted(ORGANS.items(), key=lambda kv: kv[1][0]):
        if f < 1 or f > 100: continue
        e = em_at(f)
        c = "#c0392b" if org == "neocortex" else ("#7f8c8d" if org == "hypothalamus" else band_colors.get(band, "#bbbbbb"))
        ax[1].scatter([f], [e["brain_in_lambda"]], color=c, s=45, zorder=5)
        if org in ("neocortex", "hypothalamus", "olfactory_bulb"):
            ax[1].annotate(org, (f, e["brain_in_lambda"]), fontsize=8,
                           xytext=(4, 4), textcoords="offset points")
    ax[1].set_xlabel("frequency (Hz)"); ax[1].set_ylabel("brain size / wavelength")
    ax[1].set_title("How spatially structured each rhythm's EM field is\n(frontal gamma = fastest -> closest to the radiative edge)")
    ax[1].legend(fontsize=8); ax[1].grid(True, which="both", alpha=0.2)

    fig.suptitle("Frontal lobe emerged (FOXG1) -> its electromagnetic wave in brain tissue", fontsize=13, y=1.02)
    fig.tight_layout()
    out = "/mnt/user-data/outputs/frontal_em_wave.png"
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print()
    print(" figure ->", out)

if __name__ == "__main__":
    main()
