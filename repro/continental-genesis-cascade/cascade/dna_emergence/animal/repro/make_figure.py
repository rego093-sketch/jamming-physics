#!/usr/bin/env python3
"""make_figure.py -- the 3-panel DNA-emergence figure.
   A: material partitions into two kinds (gamma per gene, 6 taxa, empty no-man's-land)
   B: the two channels are decoupled (subs vs |d gamma|, r ~ 0)
   C: STATE face -- adaptive loci materially conserved, difference is a localized switch state

   results/{orthologs,channel_records}.json + data/nuc/*.gb  ->  figures/fig_dna_emergence.png
"""
import json, math, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statistics import mean
from Bio import SeqIO
from vp_gamma_engine import gamma

HERE = os.path.dirname(os.path.abspath(__file__))
RES  = os.path.join(HERE, "..", "results")
FIG  = os.path.join(HERE, "..", "figures")
NUC  = os.path.join(HERE, "data", "nuc")

rec = json.load(open(os.path.join(RES, "channel_records.json")))
O   = json.load(open(os.path.join(RES, "orthologs.json")))
GENES = ["ND1","ND2","COX1","COX2","ATP8","ATP6","COX3","ND3","ND4L","ND4","ND5","ND6","CYTB"]
ELE = ["mammoth","asian_elephant","african_elephant"]; HOM = ["human","neanderthal","denisovan"]

def pearson(a, b):
    n = len(a); ma, mb = mean(a), mean(b)
    num = sum((x-ma)*(y-mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b))
    return num/den if den else float('nan')

def cds(name):
    r = SeqIO.read(os.path.join(NUC, name + ".gb"), "genbank")
    f = [x for x in r.features if x.type == "CDS"][0]
    return str(f.extract(r.seq)).upper()

def main():
    fig, ax = plt.subplots(1, 3, figsize=(16, 5.2))
    C = {"Elephantidae":"#1f6f4f", "Homo":"#7a3b8f"}

    # Panel A: two-band material partition
    ax0 = ax[0]
    gmean = mean([gamma(O[t]['genes'][gn]) for t in ELE+HOM for gn in GENES])
    for gi, gn in enumerate(GENES):
        ev = [gamma(O[t]['genes'][gn]) for t in ELE]; hv = [gamma(O[t]['genes'][gn]) for t in HOM]
        ax0.scatter([gi]*3, ev, c=C["Elephantidae"], s=26, zorder=3)
        ax0.scatter([gi]*3, hv, c=C["Homo"], s=26, marker="s", zorder=3)
    ax0.axhline(gmean, ls="--", c="#999", lw=1.2)
    ax0.text(12.3, gmean+0.001, "global mean\n(no kind lives here)", fontsize=8, color="#777", ha="right")
    ax0.set_xticks(range(13)); ax0.set_xticklabels(GENES, rotation=90, fontsize=8)
    ax0.set_ylabel("VP material  gamma = -mean(NN stacking dG)")
    ax0.set_title("A. Material partitions into two kinds\n(per-gene gap / within-kind spread: median 17x)", fontsize=10)
    ax0.scatter([], [], c=C["Elephantidae"], label="Elephantidae (mammoth/Asian/African)")
    ax0.scatter([], [], c=C["Homo"], marker="s", label="Homo (human/Neander./Deniso.)")
    ax0.legend(fontsize=8, loc="center right")

    # Panel B: decoupling scatter
    ax1 = ax[1]
    for cl, col in C.items():
        xs = [r["subs"] for r in rec if r["clade"] == cl]; ys = [r["dgamma"] for r in rec if r["clade"] == cl]
        ax1.scatter(xs, ys, c=col, s=22, alpha=.75, label=f"{cl} (r={pearson(xs,ys):+.2f})")
    allx = [r["subs"] for r in rec]; ally = [r["dgamma"] for r in rec]
    ax1.set_xlabel("substitutions per gene-pair  (the molecular-clock channel)")
    ax1.set_ylabel("|d gamma|  (the material channel)")
    ax1.set_title(f"B. The two channels are decoupled\noverall r(subs, |d gamma|) = {pearson(allx,ally):+.2f}  (n={len(rec)})", fontsize=10)
    ax1.legend(fontsize=8)

    # Panel C: STATE face
    ax2 = ax[2]
    loci = {"HBB/D\n(cold Hb)": (["HBB_mammoth","HBB_asian","HBB_african"], "3 AA: A13T,S87A,Q102E"),
            "MC1R\n(coat switch)": (["MC1R_mammoth_hap1","MC1R_mammoth_hap2","MC1R_asian"], "3 AA: T21A,R67C,R301S")}
    xt = []; xl = []; xpos = 0
    for lab, (names, note) in loci.items():
        gs = [gamma(cds(n)) for n in names]
        cols = ["#1f6f4f","#3a9b6f","#7fbf9f"] if "HBB" in lab else ["#7a3b8f","#a85fc0","#c89fd8"]
        ax2.scatter([xpos]*len(gs), gs, c=cols[:len(gs)], s=60, zorder=3)
        ax2.annotate(f"d_gamma={max(gs)-min(gs):.4f}\n{note}", xy=(xpos, min(gs)),
                     xytext=(xpos, min(gs)-0.012), ha="center", fontsize=7.5,
                     arrowprops=dict(arrowstyle="-", color="#bbb", lw=0.6))
        xt.append(xpos); xl.append(lab); xpos += 1
    ax2.set_xticks(xt); ax2.set_xticklabels(xl, fontsize=9)
    ax2.set_xlim(-0.6, len(loci)-0.4); ax2.set_ylim(1.45, 1.55); ax2.set_ylabel("VP material  gamma")
    ax2.set_title("C. STATE face: adaptive loci\nmaterial conserved; difference is a localized switch state", fontsize=10)

    plt.tight_layout()
    os.makedirs(FIG, exist_ok=True)
    out = os.path.join(FIG, "fig_dna_emergence.png")
    plt.savefig(out, dpi=140, bbox_inches="tight")
    print("saved figures/fig_dna_emergence.png")

if __name__ == "__main__":
    main()
