"""
demo_morpho_plus.py -- the EXPANDED gene-clock morphogenesis demo.

Grows four organisms from an egg with the gene clock driving feature emergence, using the
EXTENDED measured gamma table (42 genes). Produces, per organism:
  * a gene-coloured growth montage (crisp triangle render; each surface patch tinted by the
    master gene that built it),
  * the emergence schedule a_f(tau) (each feature switches on at its gene's R19 spinodal),
  * global + per-feature convergence to the scanned coordinates,
and across organisms:
  * morpho_heroes.png      -- the four final forms, gene-coloured, with a shared gene legend,
  * morpho_heterochrony.png-- four DNA-derived emergence timelines side by side,
  * morpho_plus.json       -- every schedule/order/convergence + the DNA-sensitivity test.

Headline that is preserved: at tau=1 every a_f=1, sigma_res=0 -> phi = full target ->
RMS small & Chamfer -> 0 for ALL four organisms (the convergence proof survives the richer
atlas). What is NEW: the order of HAIR / TEETH / IRIS / FINS / LIMBS / DIGITS / BEAK /
FEATHERS / WHISKERS appearance is now an emergent, falsifiable readout of measured DNA.
"""
import os, io, json, hashlib, contextlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import gene_clock as GC
import feature_atlas_plus as FA
import grow_gene_clock as GG
import render_plus as RP

# use the EXTENDED measured gamma table everywhere (grow_gene_clock calls GC.load_gamma)
GC.load_gamma = GC.load_gamma_table

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
os.makedirs(RES, exist_ok=True)

# resolution per organism (balance detail vs load); box sizes differ a lot
VOX = {"human_head": 0.48, "bird": 0.50, "quadruped": 0.60, "fish": 0.50}
NSTAGES = 9
VIEW = {  # (az, el) hero view per organism
    "human_head": (26, 8), "bird": (38, 16), "quadruped": (35, 14), "fish": (30, 18),
}
TITLE = {
    "human_head": "Human head (13 master genes: hair, brow, lash, iris, teeth, ...)",
    "bird": "Bird (beak=BMP4, wings=TBX5, legs=TBX4, feet=HOXD13, feathers=EDAR)",
    "quadruped": "Quadruped (forelegs=TBX5, hindlegs=TBX4, paws=HOXD13, whiskers=LEF1, coat=EDAR)",
    "fish": "Fish (pectoral=TBX5, pelvic=TBX4, median fins=SHH, gills=SOX9, scales=EDAR)",
}


def gene_order(sched):
    return list(dict.fromkeys([sched["features"][f]["gene"] for f in sched["order"]]))


def dna_sensitivity(ft, gammas, target_gene, to_gene):
    """Falsifiable: lower `target_gene` gamma to just under `to_gene` -> the emergence order
    deterministically resorts. Returns baseline & perturbed gene orders + the gammas moved."""
    base = gene_order(GC.feature_schedule(ft.features, gammas))
    g2 = dict(gammas); g2[target_gene] = gammas[to_gene] - 0.02
    new = gene_order(GC.feature_schedule(ft.features, g2))
    return dict(moved_gene=target_gene, baseline_gamma=round(gammas[target_gene], 4),
                perturbed_gamma=round(g2[target_gene], 4),
                baseline_order=base, perturbed_order=new)


SENS = {  # which gene to perturb, and below which gene, per organism
    "human_head": ("LHX2", "TP63"),    # move the (last) nose to nearly first
    "bird": ("TBX4", "EDAR"),          # move the (last) legs to nearly first
    "quadruped": ("TBX4", "EDAR"),     # hindlegs -> early
    "fish": ("TBX4", "EDAR"),          # pelvic fins -> early
}


def grow_one(name):
    ft = FA.ATLAS[name]()
    with contextlib.redirect_stdout(io.StringIO()):
        stages, info, sched = GG.grow_gene_clock(ft, vox=VOX[name], n_stages=NSTAGES)
    return ft, stages, info, sched


def fig_organism(name, ft, stages, info, sched):
    """Per-organism figure: gene-coloured growth montage + schedule + convergence."""
    final = stages[-1]
    fit = RP.fit_from(final["verts_f"], *VIEW[name], 460, 460, zoom=0.92)
    show = [0, 2, 4, 6, 8] if len(stages) >= 9 else list(range(len(stages)))
    show = [i for i in show if i < len(stages)]

    fig = plt.figure(figsize=(16.0, 9.2))
    g = fig.add_gridspec(3, len(show), height_ratios=[1.35, 1.0, 0.95],
                         hspace=0.52, wspace=0.04)

    for col, i in enumerate(show):
        s = stages[i]
        img = RP.render_stage(ft, s, fit, az=VIEW[name][0], el=VIEW[name][1])
        ax = fig.add_subplot(g[0, col]); ax.imshow(img); ax.axis("off")
        npres = sum(1 for a in s["present"].values() if a > 0.5)
        ax.set_title(f"tau={s['tau']:.2f}\nRMS {s['rms']:.2f} | {npres}/{len(s['present'])} feats",
                     fontsize=10)

    # --- emergence schedule a_f(tau), coloured by gene ---
    axs = fig.add_subplot(g[1, :])
    taus = sched["taus"]
    drawn = set()
    for fname, gene in ft.features:
        d = sched["features"][fname]
        lbl = gene if gene not in drawn else None
        drawn.add(gene)
        axs.plot(taus, d["a"], color=RP.GENE_COLOR.get(gene, "k"), lw=1.5, label=lbl, alpha=0.9)
        axs.axvline(d["tau_on"], color=RP.GENE_COLOR.get(gene, "k"), lw=0.5, ls=":", alpha=0.3)
    axs.set_xlim(0, 1); axs.set_ylim(-0.02, 1.05)
    axs.set_xlabel("developmental time  tau"); axs.set_ylabel("feature presence  a_f")
    axs.set_title("gene clock: each feature switches ON at a tau set by its master gene's R19 "
                  "spinodal (measured gamma)\nemergence ORDER is a DNA readout  |  order:  "
                  + " > ".join(gene_order(sched)), fontsize=10.5)
    axs.legend(ncol=8, fontsize=7.5, loc="upper left", frameon=False)

    # --- convergence ---
    axc = fig.add_subplot(g[2, :])
    ts = [s["tau"] for s in stages]
    axc.plot(ts, [s["rms"] for s in stages], "o-", color="#111", lw=2, label="global surface RMS")
    axc.plot(ts, [s["chamfer"] for s in stages], "s--", color="#777", lw=1.6, label="global Chamfer")
    # a few representative per-feature curves
    reps = [f for f, _ in ft.features][:0]
    for fname in _rep_features(name, ft):
        gene = dict(ft.features)[fname]
        ys = [s["feature_rms"].get(fname) for s in stages]
        xs2 = [t for t, y in zip(ts, ys) if y is not None]
        ys2 = [y for y in ys if y is not None]
        if xs2:
            axc.plot(xs2, ys2, ".-", color=RP.GENE_COLOR.get(gene, "k"), lw=1.0, alpha=0.8,
                     label=f"{fname}")
    axc.set_xlim(0, 1); axc.set_ylim(bottom=-0.05)
    axc.set_xlabel("developmental time  tau"); axc.set_ylabel("error -> 0")
    axc.set_title(f"convergence: the form reaches the scanned coordinates  "
                  f"(final RMS {final['rms']:.3f}, Chamfer {final['chamfer']:.4f})", fontsize=10.5)
    axc.legend(ncol=5, fontsize=7.5, frameon=False)

    fig.suptitle(f"{TITLE[name]}\none R19 switch across packages "
                 f"(|delta|={info['one_switch_delta']:.0e}); feature timing IS measured DNA",
                 fontsize=12.5, y=0.995)
    out = os.path.join(RES, f"morpho_{name}.png")
    fig.savefig(out, dpi=110, bbox_inches="tight"); plt.close(fig)
    return out


def _rep_features(name, ft):
    picks = {
        "human_head": ["eye_L", "nose_tip", "hair_crown", "teeth_up", "lips"],
        "bird": ["beak_up", "wing_L", "leg_L", "foot_L", "eye_L"],
        "quadruped": ["leg_foreL", "leg_hindL", "paw_foreL", "whisker_L", "eye_L"],
        "fish": ["pectoral_L", "pelvic_L", "dorsal", "caudal", "eye_L"],
    }
    have = {n for n, _ in ft.features}
    return [p for p in picks.get(name, []) if p in have]


def fig_heroes(grown):
    """Four final forms, gene-coloured crisp renders, with a shared gene legend."""
    fig = plt.figure(figsize=(15.5, 5.2))
    gs = fig.add_gridspec(1, 4, wspace=0.03)
    used = set()
    for col, name in enumerate(["human_head", "bird", "quadruped", "fish"]):
        ft, stages, info, sched = grown[name]
        final = stages[-1]
        fit = RP.fit_from(final["verts_f"], *VIEW[name], 520, 560, zoom=0.95)
        img = RP.render_stage(ft, final, fit, az=VIEW[name][0], el=VIEW[name][1])
        ax = fig.add_subplot(gs[0, col]); ax.imshow(img); ax.axis("off")
        ax.set_title(name.replace("_", " "), fontsize=12)
        cen = final["verts_f"][final["faces"]].mean(1)
        used |= set(RP.face_genes(ft, final["present"], cen).tolist())
    order = ["PAX6", "PAX2", "LHX2", "MITF", "TP63", "FOXG1", "SHH", "MYOD1", "POU2F3",
             "EDAR", "FOXN1", "HOXC13", "LEF1", "PAX9", "TBX5", "TBX4", "HOXD13", "BMP4",
             "SOX9", "SKIN"]
    handles = RP.legend_handles([g for g in order if g in used])
    fig.legend(handles=handles, loc="lower center", ncol=10, fontsize=8.5, frameon=False,
               bbox_to_anchor=(0.5, -0.06))
    fig.suptitle("One engine, one R19 switch, measured DNA -> four bodies. "
                 "Each surface patch is coloured by the master gene that built it.",
                 fontsize=13, y=1.02)
    out = os.path.join(RES, "morpho_heroes.png")
    fig.savefig(out, dpi=120, bbox_inches="tight"); plt.close(fig)
    return out


def fig_heterochrony(grown):
    """Four DNA-derived emergence timelines: gene markers placed at their tau_on."""
    names = ["human_head", "bird", "quadruped", "fish"]
    fig, axes = plt.subplots(len(names), 1, figsize=(13.5, 8.4))
    for ax, name in zip(axes, names):
        ft, stages, info, sched = grown[name]
        # one marker per gene at the mean tau_on of its features
        gtau = {}
        for fname, gene in ft.features:
            gtau.setdefault(gene, []).append(sched["features"][fname]["tau_on"])
        items = sorted(((np.mean(v), k) for k, v in gtau.items()))
        for t, gene in items:
            ax.scatter([t], [0], s=240, color=RP.GENE_COLOR.get(gene, "k"), zorder=3,
                       edgecolors="white", linewidths=1.2)
            ax.annotate(gene, (t, 0), rotation=40, fontsize=8.5, ha="left", va="bottom",
                        xytext=(2, 6), textcoords="offset points")
        ax.plot([0, 1], [0, 0], color="#ccc", lw=2, zorder=1)
        ax.set_xlim(-0.02, 1.05); ax.set_ylim(-0.5, 0.8)
        ax.set_yticks([]); ax.set_ylabel(name.replace("_", " "), fontsize=10, rotation=0,
                                         ha="right", va="center")
        if name != names[-1]:
            ax.set_xticklabels([])
    axes[-1].set_xlabel("developmental time  tau   (gene switches ON at its R19 spinodal of measured gamma)")
    fig.suptitle("Heterochrony as a DNA readout: emergence ORDER = argsort(spinodal(gamma)).  "
                 "Perturb a gamma and the order resorts (falsifiable).", fontsize=12.5, y=0.98)
    fig.tight_layout(rect=[0.04, 0, 1, 0.95])
    out = os.path.join(RES, "morpho_heterochrony.png")
    fig.savefig(out, dpi=120, bbox_inches="tight"); plt.close(fig)
    return out


def main():
    one_switch = GC.assert_one_switch()
    gammas, prov = GC.load_gamma_table()

    grown = {}
    figs = []
    for name in ["human_head", "bird", "quadruped", "fish"]:
        ft, stages, info, sched = grow_one(name)
        grown[name] = (ft, stages, info, sched)
        figs.append(fig_organism(name, ft, stages, info, sched))
        print(f"[{name}] grid {info['grid']} voxels {info['voxels']:,}  "
              f"RMS {stages[0]['rms']:.2f}->{stages[-1]['rms']:.3f}  "
              f"Chamfer {stages[-1]['chamfer']:.4f}  order: {' > '.join(gene_order(sched))}")

    figs.append(fig_heroes(grown))
    figs.append(fig_heterochrony(grown))

    # ---- JSON payload (deterministic) ----
    payload = dict(
        one_switch_delta=one_switch,
        n_genes=len(gammas),
        gamma_provenance=prov[:400],
        sign_convention="higher spinodal -> later tau_on (neuro Organ convention) [F]",
        organisms={},
    )
    for name in grown:
        ft, stages, info, sched = grown[name]
        s, t = SENS[name]
        payload["organisms"][name] = dict(
            n_features=len(ft.features),
            grid=info["grid"], voxels=info["voxels"],
            gene_order=gene_order(sched),
            order_is_gamma_readout=sched["order_is_gamma_readout"],
            features={f: dict(gene=sched["features"][f]["gene"],
                              gamma=round(sched["features"][f]["gamma"], 4),
                              spinodal=round(sched["features"][f]["spinodal"], 4),
                              tau_on=round(sched["features"][f]["tau_on"], 3),
                              dwell=round(sched["features"][f]["dwell"], 4))
                      for f in sched["order"]},
            convergence=[dict(tau=round(st["tau"], 3), rms=round(st["rms"], 4),
                              chamfer=round(st["chamfer"], 4),
                              n_present=sum(1 for a in st["present"].values() if a > 0.5))
                         for st in stages],
            final_rms=round(stages[-1]["rms"], 4),
            final_chamfer=round(stages[-1]["chamfer"], 4),
            dna_sensitivity=dna_sensitivity(ft, gammas, s, t),
        )
    out_json = os.path.join(RES, "morpho_plus.json")
    json.dump(payload, open(out_json, "w"), indent=2)

    print("\n=== expanded gene-clock morphogenesis ===")
    print(f"one R19 switch across packages: |delta| = {one_switch:.2e}")
    print(f"measured genes in atlas: {len(gammas)}")
    for name in grown:
        sens = payload["organisms"][name]["dna_sensitivity"]
        print(f"  [{name}] DNA sensitivity: {sens['moved_gene']} "
              f"{sens['baseline_gamma']}->{sens['perturbed_gamma']}")
        print(f"      baseline : {' > '.join(sens['baseline_order'])}")
        print(f"      perturbed: {' > '.join(sens['perturbed_order'])}")
    for f in figs:
        print("wrote", f)
    print("wrote", out_json)
    return payload


if __name__ == "__main__":
    main()
