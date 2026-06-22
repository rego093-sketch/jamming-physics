# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- CORTICAL (FRONTAL) SUBSTRATE EMERGENCE
#  Constitution: 4D-DNA emergence, NO TUNING, no arbitrary setting.
#
#  The F1 probe VIOLATED no-tuning: it READ the atlas band (neocortex f0=40 Hz,
#  a Fries-2009 citation) and DROVE the node at 40 Hz. A cited measurement is
#  still an INPUT read off a table, not a frequency EMERGED from the gene.
#
#  Here the ONLY grounded input is the measured master-gene gamma
#  (FOXG1 = 1.4737, SantaLucia-1998 NN dG37, NCBI RefSeq GRCh38, read-only).
#  The rhythm is EMERGED from the FHN cell via the frozen Population machinery
#  (the SAME code emerge_brainwave uses). The atlas 40 Hz is used ONLY as a
#  VALIDATION TARGET (compare emerged-vs-cited), never as an input.
#
#  new_tuned_constants = 0. Frequency is a pure function of (gene gamma,
#  inhibitory recovery tau); both are grounded; nothing is fit to a target.
# ==========================================================================
import sys, os, math
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import vp_mind_engine as E          # FROZEN, READ-ONLY (sha e61083ae...)

# --------------------------------------------------------------------------
#  GROUNDED INPUTS (the only two kinds the engine itself uses)
# --------------------------------------------------------------------------
ATLAS = E.load_brain_atlas()        # read-only data file

def gene(organ):
    e = ATLAS["organs"][organ]
    return dict(master=e["master"], gamma=float(e["gamma"]),
                f0_cited_hz=float(e.get("f0_hz", float("nan"))),
                band_cited=e.get("band", ""))

# Canonical inhibitory recovery constants -- IDENTICAL to the frozen
# emerge_brainwave(): slow inhibition (GABA_B-like) and fast inhibition
# (GABA_A-like). These are cell-type kinetics, not free knobs. NO new constant.
TAU_SLOW = 60.0    # -> low band (theta-like)   [emerge_brainwave verbatim]
TAU_FAST = 6.0     # -> high band (gamma-like)  [emerge_brainwave verbatim]

# --------------------------------------------------------------------------
#  EMERGENCE: rhythm out of the gene's FHN cell (nothing set to a target)
# --------------------------------------------------------------------------
def emerge_freq(gamma_gene, tau_inh):
    """Frequency EMERGED from the R19+FHN population: dominant_freq of the LFP.
       Pure function of (gene gamma, inhibitory tau). drive=0 -> autonomous
       relaxation oscillation. This is the frozen Population code, parameterised
       by the organ's OWN measured gamma."""
    pop = E.Population(gamma=float(gamma_gene))
    out = pop.lfp(tau_inh=float(tau_inh))     # drive defaults to 0.0
    return float(out["freq"])

def emerge_organ(organ):
    g = gene(organ)
    f_theta = emerge_freq(g["gamma"], TAU_SLOW)
    f_gamma = emerge_freq(g["gamma"], TAU_FAST)
    wm = f_gamma / f_theta if f_theta > 0 else float("nan")
    return dict(
        organ=organ, master=g["master"], gamma_gene=g["gamma"],
        spinodal=float(E.spinodal(g["gamma"])),     # developmental-order key
        barrier=float(E.barrier(g["gamma"])),       # attractor stability
        f_slow_emerged=f_theta,                      # theta-like, model units
        f_fast_emerged=f_gamma,                      # gamma-like, model units
        wm_capacity_emerged=wm,                      # theta/gamma nesting (items)
        f0_cited_hz=g["f0_cited_hz"], band_cited=g["band_cited"],
    )

def tau_sweep(gamma_gene, taus):
    """Anti-tuning: the emergent frequency-vs-tau curve. Confirms the band is a
       monotone EMERGENT response to inhibitory kinetics, not a set point."""
    return [(float(t), emerge_freq(gamma_gene, t)) for t in taus]

# --------------------------------------------------------------------------
#  REPORT
# --------------------------------------------------------------------------
def main():
    print("=" * 74)
    print(" vp_frontal v2 -- cortical rhythm EMERGED from FOXG1 (NO TUNING)")
    print(" only input: measured gene gamma + canonical GABA tau (emerge_brainwave)")
    print("=" * 74)

    cx = emerge_organ("neocortex")    # FOXG1 -- the frontal/cortical substrate
    hp = emerge_organ("hippocampus")  # LHX2  -- known engine result, as a control

    for r in (cx, hp):
        print()
        print("ORGAN: {}   master={} (gene gamma={:.4f}, MEASURED read-only)".format(
            r["organ"], r["master"], r["gamma_gene"]))
        print("  4D-DNA fold     : spinodal={:.4f}  barrier={:.4f}".format(
            r["spinodal"], r["barrier"]))
        print("  EMERGED rhythm  : f_slow={:.4f}  f_fast={:.4f}  (model units)".format(
            r["f_slow_emerged"], r["f_fast_emerged"]))
        print("  EMERGED WM cap  : f_fast/f_slow = {:.4f} items (theta/gamma nesting)".format(
            r["wm_capacity_emerged"]))
        print("  cited band      : {:.1f} Hz ({})  <- VALIDATION TARGET, NOT input".format(
            r["f0_cited_hz"], r["band_cited"]))

    print()
    print("-" * 74)
    print(" VALIDATION (emerged vs cited -- the gene was never told the band):")
    print("   neocortex cited gamma 40 Hz, hippocampus cited theta 7 Hz -> ratio 40/7 = {:.3f}".format(40.0/7.0))
    print("   engine emerge_memory WM capacity (theta/gamma)            = 6.125 items")
    print("   EMERGED neocortex WM capacity                             = {:.3f} items".format(cx["wm_capacity_emerged"]))
    print("   EMERGED hippocampus WM capacity                           = {:.3f} items".format(hp["wm_capacity_emerged"]))
    print("   band identity (f_fast > f_slow) emerges for both          : {}".format(
        bool(cx["f_fast_emerged"] > cx["f_slow_emerged"] and hp["f_fast_emerged"] > hp["f_slow_emerged"])))

    print()
    print("-" * 74)
    print(" ANTI-TUNING: emergent frequency vs inhibitory tau (neocortex/FOXG1)")
    print("   (a single tau is never picked to hit 40 Hz; the whole curve is shown)")
    for t, f in tau_sweep(cx["gamma_gene"], [6, 10, 20, 30, 45, 60, 90]):
        print("     tau_inh={:5.1f}  ->  f_emerged={:.4f}".format(t, f))

    print()
    print(" GRADES:  gene gamma [F measured] | band identity & WM-capacity ratio [V] |")
    print("          absolute Hz (needs time-unit calibration bridge) [O]")
    print(" new_tuned_constants = 0 | frequency EMERGED, never set | engine READ-ONLY")

if __name__ == "__main__":
    main()
