#!/usr/bin/env python3
"""make_figure.py -- the 3-panel plant figure.
   A: plastid material is conserved ACROSS kinds (grass vs nightshade band centres coincide; rbcL spotlight)
   B: clock/material decoupling in plants (subs vs |dgamma|, r ~ 0)
   C: cold-vs-UV STATE face -- gamma tracks LINEAGE (grass vs dicot), not environment

   results/* + data/stress/*  ->  figures/fig_plant_emergence.png
"""
import json, math, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statistics import mean
from Bio import SeqIO
from vp_gamma_engine import gamma, gc_frac

HERE = os.path.dirname(os.path.abspath(__file__))
RES  = os.path.join(HERE, "..", "results")
FIG  = os.path.join(HERE, "..", "figures")
ST   = os.path.join(HERE, "data", "stress")

def cds(name):
    rec = SeqIO.read(os.path.join(ST, name + ".gb"), "genbank")
    f = [x for x in rec.features if x.type == "CDS"][0]
    return str(f.extract(rec.seq)).upper()

def pearson(a, b):
    n = len(a); ma, mb = mean(a), mean(b)
    num = sum((x-ma)*(y-mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b))
    return num/den if den else float("nan")

def main():
    O = json.load(open(os.path.join(RES, "plastid_orthologs.json")))
    rec = json.load(open(os.path.join(RES, "plant_channel_records.json")))
    TAXA = ["rice", "maize", "wheat", "tobacco", "tomato", "potato"]
    GRASS = ["rice", "maize", "wheat"]; SOLAN = ["tobacco", "tomato", "potato"]
    GENES = sorted(O["rice"]["genes"])
    Cg, Cs = "#1f6f4f", "#b06a1f"

    fig, ax = plt.subplots(1, 3, figsize=(16, 5.2))

    # Panel A: plastid conserved across kinds
    ax0 = ax[0]
    gall = [gamma(O[t]['genes'][gn]) for t in GRASS for gn in GENES]
    sall = [gamma(O[t]['genes'][gn]) for t in SOLAN for gn in GENES]
    ax0.hist(gall, bins=24, alpha=0.6, color=Cg, label=f"grasses (centre {mean(gall):.4f})")
    ax0.hist(sall, bins=24, alpha=0.6, color=Cs, label=f"nightshades (centre {mean(sall):.4f})")
    ax0.axvline(mean(gall), color=Cg, lw=1.4); ax0.axvline(mean(sall), color=Cs, lw=1.4, ls="--")
    ax0.set_xlabel("VP material  gamma"); ax0.set_ylabel("plastid genes")
    ax0.set_title(f"A. Plastid material conserved ACROSS kinds\nband centres differ by only {abs(mean(gall)-mean(sall)):.4f}  (animals: ~0.07)", fontsize=10)
    ax0.legend(fontsize=8)

    # Panel B: clock decoupling
    ax1 = ax[1]
    for kind, col in [("Poaceae", Cg), ("Solanaceae", Cs)]:
        xs = [r["subs"] for r in rec if r["kind"] == kind]; ys = [r["dgamma"] for r in rec if r["kind"] == kind]
        ax1.scatter(xs, ys, c=col, s=14, alpha=.55, label=f"{kind} (r={pearson(xs,ys):+.2f})")
    allx = [r["subs"] for r in rec]; ally = [r["dgamma"] for r in rec]
    ax1.set_xlabel("substitutions per gene-pair  (the molecular-clock channel)")
    ax1.set_ylabel("|d gamma|  (the material channel)")
    ax1.set_title(f"B. Clock and material decoupled (plants too)\noverall r = {pearson(allx,ally):+.2f}  (n={len(rec)})", fontsize=10)
    ax1.legend(fontsize=8)

    # Panel C: cold-vs-UV STATE face -- gamma tracks lineage, not environment
    ax2 = ax[2]
    chs = {"barley\n(COLD grass)": ("CHS_barley", Cg), "maize\n(WARM grass)": ("CHS_maize", Cg),
           "arabidopsis\n(temp dicot)": ("CHS_arabidopsis", Cs), "grape\n(HIGH-UV dicot)": ("CHS_grape", Cs),
           "snapdragon\n(dicot)": ("CHS_snapdragon", Cs), "petunia\n(dicot)": ("CHS_petunia", Cs)}
    xt = []; xl = []
    for i, (lab, (fn, col)) in enumerate(chs.items()):
        g = gamma(cds(fn))
        ax2.scatter([i], [g], c=col, s=80, zorder=3)
        xt.append(i); xl.append(lab)
    ax2.set_xticks(xt); ax2.set_xticklabels(xl, fontsize=7.5)
    ax2.set_ylabel("VP material  gamma  (CHS, the UV switch)")
    ax2.set_title("C. CHS gamma tracks LINEAGE, not environment\ncold & warm grasses both high; dicots lower (any habitat)", fontsize=10)
    ax2.scatter([], [], c=Cg, label="grass lineage")
    ax2.scatter([], [], c=Cs, label="dicot lineage")
    ax2.legend(fontsize=8, loc="upper right")

    plt.tight_layout()
    os.makedirs(FIG, exist_ok=True)
    plt.savefig(os.path.join(FIG, "fig_plant_emergence.png"), dpi=140, bbox_inches="tight")
    print("saved figures/fig_plant_emergence.png")

if __name__ == "__main__":
    main()
