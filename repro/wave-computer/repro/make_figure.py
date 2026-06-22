#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the 4-panel wave-compute atlas figure from wave_compute_results.json."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_compute_results.json"))

fig, ax = plt.subplots(2, 2, figsize=(12.6, 9.2))
fig.suptitle("vp_wave_computer v0.1 — wave-substrate compute (phase carries the datum)\n"
             "store / compute / pattern on one medium, then noise-robust comms  —  "
             "consciousness_claim=0, new_tuned_constants=0",
             fontsize=12.5, fontweight="bold")

# ---- D1: storage capacity ----
a = ax[0, 0]
cap = r["D1_capacity"]
al = [c["alpha"] for c in cap]
rc = [c["recall_success"] for c in cap]
sd = [c["recall_success_sd"] for c in cap]
a.errorbar(al, rc, yerr=sd, marker="o", lw=2, capsize=3, color="#1f5fa6")
a.axhline(0.90, ls=":", color="grey", lw=1)
ac = r["headline"]["storage_capacity_alpha_c"]
a.axvline(ac, ls="--", color="#c0392b", lw=1.4,
          label=f"capacity $\\alpha_c$≈{ac:.2f}  (~{int(round(ac*256))}/256)")
a.set_title("D1 — STORAGE: patterns as phase attractors", fontweight="bold", fontsize=11)
a.set_xlabel("load  $\\alpha = P/N$  (patterns per oscillator)")
a.set_ylabel("clean-cue recall success")
a.set_ylim(-0.04, 1.06)
a.legend(fontsize=9, loc="lower left")
a.grid(alpha=0.25)

# ---- D2: basins ----
b = ax[0, 1]
cur = r["D2_basins"]["curve"]
ff = [c["flip_frac"] for c in cur]
fin = [c["final_overlap"] for c in cur]
ini = [c["init_overlap"] for c in cur]
b.plot(ff, ini, marker="s", lw=1.6, ls="--", color="#999999", label="cue (before settling)")
b.plot(ff, fin, marker="o", lw=2.2, color="#1f7a3d", label="recovered (after settling)")
b.axhline(0.95, ls=":", color="grey", lw=1)
cf = r["headline"]["computation_critical_corruption_fracbits"]
b.axvline(cf, ls="--", color="#c0392b", lw=1.4, label=f"basin edge ≈{cf:.0%} bits flipped")
b.set_title("D2 — COMPUTATION: pattern completion = physics settling",
            fontweight="bold", fontsize=11)
b.set_xlabel("input corruption (fraction of bits flipped)")
b.set_ylabel("overlap with stored wave")
b.set_ylim(0, 1.06)
b.legend(fontsize=8.5, loc="lower left")
b.grid(alpha=0.25)

# ---- D3: regime ----
c = ax[1, 0]
reg = r["D3_regime"]
g = [x["gain"] for x in reg]
rec = [x["recall_overlap"] for x in reg]
c.plot(g, rec, marker="o", lw=2.2, color="#7d3c98", label="recall (computation)")
gbest = g[int(np.argmax(rec))]
c.axvline(gbest, ls="--", color="#1f7a3d", lw=1.3, label=f"interior optimum g≈{gbest}")
c.axvspan(0, 0.12, color="#c0392b", alpha=0.08)
c.text(0.02, min(rec) + 0.02, "field OFF\n(no stored\nstructure)", fontsize=8, color="#c0392b")
c.set_title("D3 — REGIME: compute lives below full coherence\n"
            "(interior coupling optimum; over-drive degrades)",
            fontweight="bold", fontsize=10.5)
c.set_xlabel("coupling-field gain  $g$  (medium stiffness)")
c.set_ylabel("recall overlap")
c.set_xscale("symlog", linthresh=0.25)
c.set_ylim(0.6, 1.03)
c.legend(fontsize=9, loc="lower left")
c.grid(alpha=0.25)

# ---- D4: BER ----
d = ax[1, 1]
com = r["D4_comm"]["curve"]
sg = [x["sigma"] for x in com]
bp = [x["ber_phase_bpsk"] for x in com]
bo = [x["ber_amplitude_ook"] for x in com]
bc = [max(x["ber_phase_plus_cleanup"], 1e-5) for x in com]
d.semilogy(sg, bo, marker="s", lw=2, color="#c0392b", label="amplitude (OOK)")
d.semilogy(sg, bp, marker="o", lw=2, color="#1f5fa6", label="phase (BPSK)")
d.semilogy(sg, bc, marker="D", lw=2.4, color="#1f7a3d",
           label="phase + attractor clean-up")
# mark negative-SNR region
for x in com:
    if x["snr_db"] < 0:
        d.axvspan(x["sigma"] - 0.1, x["sigma"] + 0.1, color="grey", alpha=0.05)
d.axvline([x["sigma"] for x in com if x["snr_db"] < 0][0] - 0.1, ls=":",
          color="grey", lw=1)
d.text(1.32, 0.0002, "noise > signal\n(SNR < 0 dB)", fontsize=8, color="#555555",
       ha="center")
d.set_title("D4 — COMMUNICATION through noise\n"
            "structured phase code stays ~error-free at negative SNR",
            fontweight="bold", fontsize=10.5)
d.set_xlabel("channel noise  $\\sigma$  (matched energy $E_s=1$)")
d.set_ylabel("bit error rate")
d.set_ylim(8e-6, 0.6)
d.legend(fontsize=9, loc="lower right")
d.grid(alpha=0.25, which="both")

fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("wave_compute_atlas.png", dpi=140, bbox_inches="tight")
print("wrote wave_compute_atlas.png")
