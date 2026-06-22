#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.10 atlas from wave_agi_results.json (L9 — THE END CONDITION: the integrated
L0-L8 wave machine assessed against the capability ladder; each rung scored pass [V] / honest
[O]; FUNCTION only). Eight panels: A1 compositional/multi-item capacity · A2 one-shot
generalization · A3 real-time adaptation (the honest [O]) · A4 noise-immersed robustness
(D4 fidelity lift) · A5 scale content-addressable memory · A6 cross-domain transfer ·
A7 open-ended acquisition · the LADDER verdict (6/7 [V], A3 the lone [O])."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_agi_results.json"))
a1, a2, a3 = r["A1_multi_item"], r["A2_one_shot"], r["A3_realtime_adapt"]
a4, a5, a6, a7 = r["A4_noise_cognition"], r["A5_scale_cam"], r["A6_cross_domain"], r["A7_open_ended"]
END, H = r["END_CONDITION"], r["headline"]
CAP = a1["inherited_theta_gamma_capacity_for_comparison"]

BLUE, GREEN, PURPLE, RED, ORANGE, GREY = \
    "#1f5fa6", "#1f7a3d", "#6a1b9a", "#c0392b", "#e08214", "#8a8a8a"

fig, ax = plt.subplots(2, 4, figsize=(23.6, 11.6))
fig.suptitle(
    "vp_wave_computer v0.10 — L9: functional general intelligence (THE END CONDITION)\n"
    "the integrated L0–L8 wave machine on the capability ladder: "
    f"{H['ladder_rungs_passed']} rungs [V]; A3 (single-store rule over-write) the lone honest [O], "
    "mitigation = the proven L5 dual store (A7)\n"
    "FIREWALL: passing the ladder is FUNCTIONAL general intelligence; the hard-problem blank stays "
    "OPEN, never erased  —  consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0",
    fontsize=11.4, fontweight="bold")

# ---------------------------------------------------------------- A1 capacity
a = ax[0, 0]
by = a1["by_config"]
for N, col in zip(sorted({c["N"] for c in by}), (BLUE, PURPLE)):
    Ks = [c["K"] for c in by if c["N"] == N]
    rec = [c["per_slot_recovery"] for c in by if c["N"] == N]
    a.plot(Ks, rec, "o-", color=col, lw=2, ms=5, label=f"N={N}")
    kstar = a1["capacity_Kstar_by_N"][str(N)]
    a.axvline(kstar, color=col, ls=":", lw=1.2, alpha=0.7)
    a.annotate(f"K*={kstar}", (kstar, 0.42), color=col, fontsize=9, ha="center")
a.axhline(0.9, color=GREY, ls="--", lw=1.2, label="recovery 0.9")
a.axvline(CAP, color=ORANGE, ls="-.", lw=1.6, alpha=0.8, label=f"θ–γ ~{CAP} (compare)")
a.set_title("A1 · compositional / multi-item  [V]\nper-slot recovery vs #items K (capacity K* EMERGES)",
            fontsize=10, fontweight="bold")
a.set_xlabel("items co-hosted in θ–γ slots, K"); a.set_ylabel("per-slot recovery")
a.set_ylim(0.0, 1.05); a.legend(fontsize=7.6, loc="lower left"); a.grid(alpha=0.25)

# ---------------------------------------------------------------- A2 one-shot
a = ax[0, 1]
by = a2["by_config"]
for nz, col in zip(sorted({c["test_noise"] for c in by}), (BLUE, GREEN, RED)):
    Bs = [c["B"] for c in by if c["test_noise"] == nz]
    acc = [c["novel_instance_acc"] for c in by if c["test_noise"] == nz]
    a.plot(Bs, acc, "o-", color=col, lw=2, ms=5, label=f"cue noise {nz:.2f}")
Bs = sorted({c["B"] for c in by}); a.plot(Bs, [1.0 / b for b in Bs], "k--", lw=1.3, label="chance 1/B")
a.set_title("A2 · one-shot generalization  [V]\nnovel-instance accuracy from ONE example",
            fontsize=10, fontweight="bold")
a.set_xlabel("#categories B"); a.set_ylabel("novel-instance accuracy")
a.set_ylim(0.0, 1.05); a.set_xscale("log", base=2); a.legend(fontsize=7.6); a.grid(alpha=0.25)

# ---------------------------------------------------------------- A3 adaptation (the [O])
a = ax[0, 2]
by = a3["by_config"]
labels = [f"shift {c['shift_frac']:.1f}" for c in by]
x = np.arange(len(by)); w = 0.26
a.bar(x - w, [c["pre_shift_acc"] for c in by], w, color=GREEN, label="pre-shift")
a.bar(x, [c["dip_after_shift_acc"] for c in by], w, color=ORANGE, label="dip @ shift")
a.bar(x + w, [c["post_adapt_acc"] for c in by], w, color=RED, label="post re-imprint")
a.axhline(0.8, color=GREY, ls="--", lw=1.4, label="recovery band 0.8")
a.set_title("A3 · real-time adaptation  [O] honest shortfall\nsingle additive store cannot OVER-WRITE a switched rule",
            fontsize=10, fontweight="bold", color=RED)
a.set_xticks(x); a.set_xticklabels(labels); a.set_ylabel("response accuracy")
a.set_ylim(0.0, 1.08); a.legend(fontsize=7.6, loc="upper right"); a.grid(alpha=0.25, axis="y")

# ---------------------------------------------------------------- A4 noise (D4 fidelity lift)
a = ax[0, 3]
by = a4["by_config"]
fl = [c["flip_noise"] for c in by]
a.plot(fl, [c["fidelity_with_cleanup"] for c in by], "o-", color=BLUE, lw=2.2, ms=6, label="WITH clean-up (D4)")
a.plot(fl, [c["fidelity_no_cleanup"] for c in by], "s--", color=GREY, lw=2, ms=5, label="raw cue (no clean-up)")
a.fill_between(fl, [c["fidelity_no_cleanup"] for c in by], [c["fidelity_with_cleanup"] for c in by],
               color=BLUE, alpha=0.12, label="D4 fidelity lift")
a.set_title("A4 · noise-immersed robustness  [V]\nclean-up LIFTS fidelity to true prototype (off-lattice corrupt_phase)",
            fontsize=10, fontweight="bold")
a.set_xlabel("cue corruption (flip fraction + jitter)"); a.set_ylabel("overlap to TRUE prototype")
a.set_ylim(0.0, 1.05); a.legend(fontsize=7.6, loc="lower left"); a.grid(alpha=0.25)

# ---------------------------------------------------------------- A5 scale CAM
a = ax[1, 0]
by = a5["by_config"]
T = [c["T"] for c in by]
a.plot(T, [c["flat_recall"] for c in by], "s--", color=GREY, lw=2, ms=5, label="flat store")
a.plot(T, [c["hier_recall"] for c in by], "o-", color=GREEN, lw=2.2, ms=6, label="hierarchical (L3)")
a.axvline(a5["flat_capacity_ceiling_T"], color=GREY, ls=":", lw=1.3,
          label=f"flat ceiling T={a5['flat_capacity_ceiling_T']}")
a.set_title("A5 · scale content-addressable memory  [V]\nhierarchy holds recall past the flat ceiling (O(1)-in-T cost)",
            fontsize=10, fontweight="bold")
a.set_xlabel("#stored items T"); a.set_ylabel("recall accuracy")
a.set_ylim(0.0, 1.05); a.legend(fontsize=7.6, loc="center right"); a.grid(alpha=0.25)

# ---------------------------------------------------------------- A6 transfer
a = ax[1, 1]
by = a6["by_config"]
J = [c["J_attributes"] for c in by]
a.plot(J, [c["within_domain_X_acc"] for c in by], "o-", color=BLUE, lw=2.2, ms=6, label="within-domain X")
a.plot(J, [c["transfer_domain_Y_acc"] for c in by], "D-", color=PURPLE, lw=2.2, ms=6, label="transfer → Y (untrained)")
a.axvline(a6["transfer_complexity_ceiling_J"], color=RED, ls=":", lw=1.4,
          label=f"ceiling J*={a6['transfer_complexity_ceiling_J']}")
a.set_title("A6 · cross-domain transfer  [V]\nstructure transfers to never-trained fillers, to a crosstalk ceiling",
            fontsize=10, fontweight="bold")
a.set_xlabel("relational complexity J (attributes)"); a.set_ylabel("accuracy")
a.set_ylim(0.0, 1.05); a.legend(fontsize=7.6, loc="lower left"); a.grid(alpha=0.25)

# ---------------------------------------------------------------- A7 open-ended
a = ax[1, 2]
by = a7["by_config"]
S = [c["n_skills"] for c in by]
a.plot(S, [c["dual_store_retention"] for c in by], "o-", color=GREEN, lw=2.2, ms=6, label="dual store (L5)")
a.plot(S, [c["single_store_retention"] for c in by], "s--", color=GREY, lw=2, ms=5, label="single store")
a.plot(S, [c["latest_skill_acc"] for c in by], "^:", color=ORANGE, lw=1.8, ms=6, label="latest-skill acc")
a.set_title("A7 · open-ended skill acquisition  [V]\ndual store keeps acquiring while retaining old (within band)",
            fontsize=10, fontweight="bold")
a.set_xlabel("#skills acquired S"); a.set_ylabel("retention / accuracy")
a.set_ylim(0.0, 1.05); a.legend(fontsize=7.6, loc="center right"); a.grid(alpha=0.25)

# ---------------------------------------------------------------- LADDER verdict
a = ax[1, 3]; a.axis("off")
grades = END["ladder_grades"]
names = {
    "A1_compositional_multi_item": "A1  compositional / multi-item",
    "A2_one_shot_generalization": "A2  one-shot generalization",
    "A3_realtime_adaptation": "A3  real-time adaptation",
    "A4_noise_immersed_robustness": "A4  noise-immersed robustness",
    "A5_scale_content_addressable_memory": "A5  scale content-addr. memory",
    "A6_cross_domain_transfer": "A6  cross-domain transfer",
    "A7_open_ended_acquisition": "A7  open-ended acquisition",
}
a.text(0.5, 0.99, "THE CAPABILITY LADDER — END CONDITION", ha="center", va="top",
       fontsize=12, fontweight="bold", transform=a.transAxes)
y = 0.90
for key, label in names.items():
    g = grades[key]
    col = GREEN if g == "[V]" else RED
    a.text(0.04, y, label, ha="left", va="center", fontsize=10.2, transform=a.transAxes)
    a.text(0.96, y, g, ha="right", va="center", fontsize=11, fontweight="bold",
           color=col, transform=a.transAxes)
    y -= 0.085
a.axhline; a.text(0.5, 0.24, f"{H['ladder_rungs_passed']} rungs [V]   ·   program_closes = {END['program_closes']}",
                  ha="center", va="center", fontsize=11.5, fontweight="bold",
                  color=BLUE, transform=a.transAxes)
a.text(0.5, 0.155,
       "the lone [O] (A3) is a single-store limit with a PROVEN\n"
       "dual-store mitigation (A7, [V]) — a stated bound, not a gap",
       ha="center", va="center", fontsize=8.6, color=RED, transform=a.transAxes)
a.text(0.5, 0.045,
       "FUNCTIONAL general intelligence — the hard-problem blank stays OPEN\n"
       "consciousness_claim = 0   ·   hard_problem_open = 1",
       ha="center", va="center", fontsize=8.8, style="italic", color=GREY,
       transform=a.transAxes,
       bbox=dict(boxstyle="round,pad=0.4", fc="#f4f4f4", ec=GREY, lw=1))

fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig("wave_agi_atlas.png", dpi=140, bbox_inches="tight")
print("wrote wave_agi_atlas.png")
