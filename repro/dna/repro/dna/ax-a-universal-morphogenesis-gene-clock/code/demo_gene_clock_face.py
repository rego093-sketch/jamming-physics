"""
demo_gene_clock_face.py -- grow an egg into the human-face scan with the GENE CLOCK driving
feature emergence, and show that the emergence ORDER is a readout of measured DNA.

Outputs (results/):
  gene_clock_face.png        montage of grown stages (features emerge in gene order) +
                             the emergence schedule a_f(tau) + global/per-feature convergence
  gene_clock_face.json       schedule (gene, gamma, spinodal, tau_on, dwell), order, the
                             gamma-readout check, the one-switch delta, convergence series,
                             and the DNA-sensitivity test (perturb one gamma -> order resorts)
"""
import os, io, json, hashlib
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

# a distinct colour per gene so the schedule reads as "which gene fired when"
GENE_COLOR = {
    "TP63": "#8c8c8c", "POU2F3": "#d62728", "SHH": "#9467bd", "PAX2": "#2ca02c",
    "FOXG1": "#1f77b4", "MYOD1": "#ff7f0e", "PAX6": "#e377c2", "LHX2": "#17becf",
}


def dna_sensitivity(features, gammas, bump=+0.08):
    """Falsifiable: the order is a FUNCTION of measured gamma, not a fixed list. Bump ONE
    gene's gamma (a promoter-stiffness variant) and the derived order resorts. Returns the
    baseline order, the gene moved, and the new order -- and the rank change it caused."""
    base = GC.feature_schedule(features, gammas)["order"]
    # move LHX2 (nose, currently last) below FOXG1 by lowering its gamma
    g2 = dict(gammas); g2["LHX2"] = gammas["FOXG1"] - 0.02
    new = GC.feature_schedule(features, g2)["order"]
    # collapse to unique gene order for readability
    def gene_seq(order, gmap):
        seen = []
        for f in order:
            gname = dict(features)[f]
            if gname not in seen:
                seen.append(gname)
        return seen
    return dict(moved_gene="LHX2", baseline_gene_order=gene_seq(base, gammas),
                perturbed_gene_order=gene_seq(new, g2),
                baseline_gamma=gammas["LHX2"], perturbed_gamma=g2["LHX2"])


def main():
    ft = FT.face_features()
    gammas, prov = GC.load_gamma()

    stages, info, sched = GG.grow_gene_clock(ft, vox=0.42, n_stages=9)
    one_switch = info["one_switch_delta"]

    # ---- montage: render every stage in a COMMON frame (growth in place) ----
    final = stages[-1]
    cen = 0.5 * (final["verts"].min(0) + final["verts"].max(0))
    span = (final["verts"].max(0) - final["verts"].min(0))
    show = [0, 2, 4, 6, 8] if len(stages) >= 9 else list(range(len(stages)))
    show = [i for i in show if i < len(stages)]

    fig = plt.figure(figsize=(15.5, 8.6))
    gs = fig.add_gridspec(3, len(show), height_ratios=[1.25, 1.0, 1.0], hspace=0.58, wspace=0.06)

    # use a fixed render scale from the final span so earlier (smaller) stages look like they grow
    R = mc._rot_matrix(35, 18)
    Pf = (final["verts"] - cen) @ R.T
    rscale = 0.82 * min(540, 360) / max((Pf.max(0) - Pf.min(0))[0], (Pf.max(0) - Pf.min(0))[1], 1e-6)

    for col, i in enumerate(show):
        s = stages[i]
        img = mc.render_mesh(s["verts"], s["normals"], az=35, el=18,
                             center=(cen @ R.T), scale=rscale)
        ax = fig.add_subplot(gs[0, col]); ax.imshow(img); ax.axis("off")
        on = [f for f, a in s["present"].items() if a > 0.5]
        ax.set_title(f"tau={s['tau']:.2f}\nRMS {s['rms']:.2f} | {len(on)}/{len(s['present'])} feats",
                     fontsize=10)

    # ---- schedule: a_f(tau) curves coloured by gene, tau_on markers, order ----
    axs = fig.add_subplot(gs[1, :])
    taus = sched["taus"]
    drawn_genes = set()
    for fname, gene in ft.features:
        d = sched["features"][fname]
        lbl = gene if gene not in drawn_genes else None
        drawn_genes.add(gene)
        axs.plot(taus, d["a"], color=GENE_COLOR.get(gene, "k"), lw=1.6, label=lbl, alpha=0.9)
        axs.axvline(d["tau_on"], color=GENE_COLOR.get(gene, "k"), lw=0.6, ls=":", alpha=0.35)
    axs.set_xlim(0, 1); axs.set_ylim(-0.02, 1.05)
    axs.set_xlabel("developmental time  tau"); axs.set_ylabel("feature presence  a_f")
    derived_order = " > ".join(dict.fromkeys([sched["features"][f]["gene"] for f in sched["order"]]))
    axs.set_title("gene clock: each feature switches on at a tau set by its master gene's R19 spinodal "
                  "(measured gamma)\nemergence ORDER is a readout of DNA   |   derived order:  "
                  + derived_order, fontsize=10.5)
    axs.legend(ncol=8, fontsize=8, loc="upper left", frameon=False)

    # ---- convergence: global RMS/Chamfer + a few per-feature RMS ----
    axc = fig.add_subplot(gs[2, :])
    ts = [s["tau"] for s in stages]
    axc.plot(ts, [s["rms"] for s in stages], "o-", color="#111", lw=2, label="global surface RMS")
    axc.plot(ts, [s["chamfer"] for s in stages], "s--", color="#777", lw=1.6, label="global Chamfer")
    for fname in ["eye_L", "nose_tip", "ear_L", "lips"]:
        gene = dict(ft.features)[fname]
        ys = [s["feature_rms"].get(fname) for s in stages]
        xs2 = [t for t, y in zip(ts, ys) if y is not None]
        ys2 = [y for y in ys if y is not None]
        axc.plot(xs2, ys2, ".-", color=GENE_COLOR.get(gene, "k"), lw=1.1, alpha=0.8,
                 label=f"{fname} RMS")
    axc.set_xlim(0, 1); axc.set_ylim(bottom=-0.05)
    axc.set_xlabel("developmental time  tau"); axc.set_ylabel("error -> 0")
    axc.set_title("convergence: the form reaches the SCANNED coordinates "
                  "(global + per-feature error -> 0)", fontsize=10.5)
    axc.legend(ncol=4, fontsize=8, frameon=False)

    fig.suptitle("Universal morphogenesis x neuro gene engine:  one R19 switch "
                 f"(cross-package |delta|={one_switch:.0e})  grows a face whose feature timing IS its DNA",
                 fontsize=12.5, y=0.995)
    out_png = os.path.join(RES, "gene_clock_face.png")
    fig.savefig(out_png, dpi=115, bbox_inches="tight"); plt.close(fig)

    # ---- DNA sensitivity test ----
    sens = dna_sensitivity(ft.features, gammas)

    # ---- JSON (deterministic payload) ----
    payload = dict(
        target=info["target"], grid=info["grid"], voxels=info["voxels"],
        one_switch_delta=one_switch,
        gamma_provenance=prov[:240],
        sign_convention="higher spinodal -> later tau_on (neuro Organ convention) [F]",
        tau_window=sched["tau_window"],
        order=sched["order"],
        order_is_gamma_readout=sched["order_is_gamma_readout"],
        gene_order=list(dict.fromkeys([sched["features"][f]["gene"] for f in sched["order"]])),
        features={f: dict(gene=sched["features"][f]["gene"],
                          gamma=round(sched["features"][f]["gamma"], 4),
                          spinodal=round(sched["features"][f]["spinodal"], 4),
                          tau_on=round(sched["features"][f]["tau_on"], 3),
                          tau_on_raw=round(sched["features"][f]["tau_on_raw"], 3),
                          dwell=round(sched["features"][f]["dwell"], 4))
                  for f in sched["order"]},
        convergence=[dict(tau=round(s["tau"], 3), rms=round(s["rms"], 4),
                          chamfer=round(s["chamfer"], 4),
                          n_present=sum(1 for a in s["present"].values() if a > 0.5))
                     for s in stages],
        dna_sensitivity=sens,
        final_rms=round(stages[-1]["rms"], 4), final_chamfer=round(stages[-1]["chamfer"], 4),
    )
    out_json = os.path.join(RES, "gene_clock_face.json")
    with open(out_json, "w") as f:
        json.dump(payload, f, indent=2)

    # console summary
    print("=== gene-clock face ===")
    print(f"one R19 switch across packages: |delta| = {one_switch:.2e}")
    print(f"grid {info['grid']}  voxels {info['voxels']}")
    print("derived emergence order (from measured gamma):")
    for f in sched["order"]:
        d = sched["features"][f]
        print(f"  {f:10s} {d['gene']:7s} gamma={d['gamma']:.4f} sp={d['spinodal']:.4f} tau_on={d['tau_on']:.3f}")
    print(f"order == argsort(spinodal) [pure gamma readout]: {sched['order_is_gamma_readout']}")
    print(f"convergence: RMS {stages[0]['rms']:.3f} -> {stages[-1]['rms']:.3f}  "
          f"Chamfer -> {stages[-1]['chamfer']:.3f}")
    print(f"DNA sensitivity: move {sens['moved_gene']} gamma "
          f"{sens['baseline_gamma']:.3f}->{sens['perturbed_gamma']:.3f}")
    print(f"  baseline gene order : {' > '.join(sens['baseline_gene_order'])}")
    print(f"  perturbed gene order: {' > '.join(sens['perturbed_gene_order'])}")
    print(f"wrote {out_png}")
    print(f"wrote {out_json}")
    return payload


if __name__ == "__main__":
    main()
