"""
demo_gene_clock_universal.py -- the SAME gene clock grows multiple body plans.

One engine (gene_clock + grow_gene_clock), three gene-tagged targets (human face, quadruped,
fish). For each: the emergence order is derived from measured gamma, and growth converges onto
the scanned coordinates (RMS -> 0). This is the "one logic, many animals" claim, now with the
schedule itself coming from DNA.

Outputs (results/):
  gene_clock_universal.png   per-organism: final grown form + its gene-derived emergence order
  gene_clock_universal.json  per-organism order, gamma-readout check, convergence
"""
import os, json, contextlib, io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import gene_clock as GC
import feature_target as FT
import grow_gene_clock as GG
import morpho_core as mc

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
os.makedirs(RES, exist_ok=True)

TARGETS = [("human face", FT.face_features, dict(vox=0.5, az=35, el=18)),
           ("quadruped", FT.quadruped_features, dict(vox=1.0, az=-58, el=18)),
           ("fish", FT.fish_features, dict(vox=0.8, az=-60, el=12))]


def main():
    fig, axes = plt.subplots(2, len(TARGETS), figsize=(15.5, 8.2),
                             gridspec_kw=dict(height_ratios=[1.3, 1.0], hspace=0.32, wspace=0.12))
    out = {}
    for j, (name, builder, opt) in enumerate(TARGETS):
        ft = builder()
        with contextlib.redirect_stdout(io.StringIO()):
            stages, info, sched = GG.grow_gene_clock(ft, vox=opt["vox"], n_stages=9)
        final = stages[-1]
        img = mc.render_mesh(final["verts"], final["normals"], az=opt["az"], el=opt["el"])
        ax = axes[0, j]; ax.imshow(img); ax.axis("off")
        ax.set_title(f"{name}\nRMS {stages[0]['rms']:.2f} -> {final['rms']:.3f}  "
                     f"(Chamfer {final['chamfer']:.3f})", fontsize=10.5)

        # gene-order schedule strip
        axs = axes[1, j]
        taus = sched["taus"]
        seen = set()
        for fname, gene in ft.features:
            d = sched["features"][fname]
            from demo_gene_clock_face import GENE_COLOR
            lbl = gene if gene not in seen else None
            seen.add(gene)
            axs.plot(taus, d["a"], color=GENE_COLOR.get(gene, "k"), lw=1.5, label=lbl)
        axs.set_xlim(0, 1); axs.set_ylim(-0.02, 1.05)
        axs.set_xlabel("tau"); 
        if j == 0: axs.set_ylabel("feature presence a_f")
        gene_order = list(dict.fromkeys([sched["features"][f]["gene"] for f in sched["order"]]))
        axs.set_title("order: " + " > ".join(gene_order), fontsize=9)
        axs.legend(ncol=3, fontsize=7, frameon=False, loc="upper left")

        out[name] = dict(order=gene_order,
                         order_is_gamma_readout=sched["order_is_gamma_readout"],
                         final_rms=round(final["rms"], 4), final_chamfer=round(final["chamfer"], 4),
                         voxels=info["voxels"])
        print(f"{name:12s}  order: {' > '.join(gene_order):45s}  "
              f"RMS->{final['rms']:.3f}  gamma-readout={sched['order_is_gamma_readout']}")

    fig.suptitle("One gene clock, many body plans: feature emergence order derived from measured "
                 "gamma; growth converges to each scan", fontsize=12.5, y=0.99)
    out_png = os.path.join(RES, "gene_clock_universal.png")
    fig.savefig(out_png, dpi=115, bbox_inches="tight"); plt.close(fig)
    json.dump(out, open(os.path.join(RES, "gene_clock_universal.json"), "w"), indent=2)
    print(f"wrote {out_png}")
    return out


if __name__ == "__main__":
    main()
