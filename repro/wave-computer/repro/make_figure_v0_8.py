#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.8 atlas from wave_embodiment_results.json (L7 embodiment / real-time control:
control = continuous settling in a closed, clock-free, end-to-end ANALOG sensorimotor loop).
Eight panels: E1 closed-loop control · E2a quantization tax · E2b dimensional advantage ·
E3 prediction-sufficiency (S7 resolved) · E4a bandwidth frontier · E4b latency/horizon frontier ·
E5a Shannon per-channel cap · E5b hybrid exact-arithmetic hand-off."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_embodiment_results.json"))
e1 = r["E1_closed_loop_control"]
e2 = r["E2_analog_io_advantage"]
e3 = r["E3_prediction_sufficiency"]
e4 = r["E4_stability_bandwidth"]
e5a = r["E5a_shannon_cap"]
e5b = r["E5b_hybrid_exact"]
h = r["headline"]

fig, ax = plt.subplots(2, 4, figsize=(23.6, 11.4))
fig.suptitle(
    "vp_wave_computer v0.8 — L7 embodiment / real-time control "
    "(control = continuous settling in a closed, clock-free, END-TO-END ANALOG loop; no ADC/DAC)\n"
    "closed-loop control · analog I/O beats ADC/DAC + dimensional advantage scales · "
    "prediction-sufficiency suffices (S7 resolved) · stable band · honest two-sides caveat  —  "
    "consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0",
    fontsize=11.6, fontweight="bold")

BLUE, GREEN, PURPLE, RED, ORANGE = "#1f5fa6", "#1f7a3d", "#6a1b9a", "#c0392b", "#e08214"

# ---- E1: closed-loop control (error vs noise; forward/reactive/open-loop) ----
a = ax[0, 0]
nc = e1["noise_curve"]
sig = [x["sigma"] for x in nc]
a.plot(sig, [x["forward_err"] for x in nc], marker="o", lw=2.8, color=GREEN,
       label="forward (anticipates +1)")
a.plot(sig, [x["reactive_err"] for x in nc], marker="s", lw=2.4, color=RED,
       label="reactive (lags by delay)")
a.plot(sig, [x["openloop_err"] for x in nc], marker="^", lw=2.0, color="#888",
       label="open-loop (drifts)")
a.set_title(f"E1 — closed-loop control by settling  {h['grade_E1_closed_loop_control']}\n"
            "(track a moving target through a 1-tick sensorimotor delay)",
            fontweight="bold", fontsize=10.2)
a.set_xlabel("sensory noise σ (graded)")
a.set_ylabel("steady-state tracking error  (1 - overlap)")
a.set_ylim(-0.04, 1.06)
a.legend(fontsize=8.4, loc="center right")
a.grid(alpha=0.25)
a.text(0.04, 0.55, "prediction\ncompensates\nloop latency", transform=a.transAxes,
       fontsize=8.0, color="#555", fontweight="bold")

# ---- E2a: quantization tax vs ADC/DAC bit depth ----
b = ax[0, 1]
tc = e2["E2a_quantization_tax_curve"]
labels = [str(x["bits"]) for x in tc]
errs = [x["err"] for x in tc]
xs = np.arange(len(tc))
cols = [RED if l == "1" else (GREEN if l == "analog" else "#888") for l in labels]
b.bar(xs, errs, color=cols, edgecolor="#333", width=0.62)
b.set_xticks(xs)
b.set_xticklabels(["1 bit", "2 bit", "3 bit", "analog"][:len(tc)])
b.set_title(f"E2a — analog I/O beats ADC/DAC  {h['grade_E2_analog_io_advantage']}\n"
            f"(graded σ={e2['tax_sigma']}; 1-bit discards noise-margin; closes at "
            f"{e2['E2a_tax_closes_at_bits']} bit)",
            fontweight="bold", fontsize=10.2)
b.set_ylabel("steady-state tracking error")
b.set_ylim(0, max(errs) * 1.25 + 0.02)
for x, e in zip(xs, errs):
    b.text(x, e + 0.004, f"{e:.3f}", ha="center", fontsize=8.4, fontweight="bold")
b.grid(alpha=0.2, axis="y")
b.text(0.5, 0.86, "the D4 noise-immunity\nadvantage at the I/O boundary",
       transform=b.transAxes, fontsize=8.0, color="#555", ha="center", fontweight="bold")

# ---- E2b: dimensional advantage (analog vs 1-bit error; aggregate N*gap) ----
c = ax[0, 2]
dc = e2["E2b_dimension_curve"]
Ns = [x["N"] for x in dc]
c.plot(Ns, [x["analog_err"] for x in dc], marker="o", lw=2.8, color=GREEN, label="analog")
c.plot(Ns, [x["onebit_err"] for x in dc], marker="s", lw=2.6, color=RED, label="1-bit ADC/DAC")
c.set_xlabel("substrate dimension N  (channels / spatial resolution)")
c.set_ylabel("tracking error", color="#333")
c.set_ylim(-0.02, max(x["onebit_err"] for x in dc) * 1.3 + 0.02)
c.legend(fontsize=8.6, loc="center left")
c2 = c.twinx()
c2.plot(Ns, [x["aggregate_advantage_N_times_gap"] for x in dc], marker="D", lw=2.6,
        color=BLUE, ls="--", label="aggregate edge = N × gap")
c2.set_ylabel("aggregate analog advantage (N × per-channel gap)", color=BLUE)
c2.tick_params(axis="y", labelcolor=BLUE)
c.set_title("E2b — dimensional advantage SCALES  [V]\n"
            "(per-channel gap stays +; aggregate N×gap grows → optical-Fourier point, E2c [O])",
            fontweight="bold", fontsize=10.2)
c.grid(alpha=0.22)

# ---- E3: prediction-sufficiency vs magnitude-identity (S7) ----
d = ax[0, 3]
n3 = e3["noise_curve"]
s3 = [x["sigma"] for x in n3]
d.plot(s3, [x["pred_sufficient_err"] for x in n3], marker="o", lw=2.8, color=GREEN,
       label=f"prediction-sufficient (L6, cos={e3['operator_L2_cosine']:.2f})")
d.plot(s3, [x["magnitude_identical_err"] for x in n3], marker="s", lw=2.4, color=BLUE,
       label="magnitude-identical (analytic L2, cos=1)")
d.set_title(f"E3 — prediction-sufficiency SUFFICES  {h['grade_E3_prediction_sufficiency']}\n"
            "(resolves the inherited S7 [O] for embodied control)",
            fontweight="bold", fontsize=10.2)
d.set_xlabel("sensory noise σ (graded)")
d.set_ylabel("steady-state tracking error")
d.set_ylim(-0.02, max(max(x["pred_sufficient_err"], x["magnitude_identical_err"])
                      for x in n3) * 1.25 + 0.02)
d.legend(fontsize=8.0, loc="upper left")
d.grid(alpha=0.25)
d.text(0.5, 0.55, "identical in the working regime;\nfull operator only marginally\nbetter at the edge of failure",
       transform=d.transAxes, fontsize=7.8, color="#555", ha="center", fontweight="bold")

# ---- E4a: bandwidth frontier ----
e = ax[1, 0]
bw = e4["E4a_bandwidth_curve"]
rates = [x["rate"] for x in bw]
e.plot(rates, [x["err"] for x in bw], marker="o", lw=2.8, color=PURPLE)
thr = e4["E4a_bandwidth_threshold_rate"]
if thr is not None:
    e.axvline(thr, ls="--", color=GREEN, lw=1.8, label=f"bandwidth threshold = {thr}")
e.axhline(0.1, ls=":", color="#a33", lw=1.2, label="track / break (err=0.1)")
e.set_title(f"E4a — control-bandwidth frontier  {h['grade_E4_stability_band']}\n"
            "(motor rate must exceed a threshold to keep up)",
            fontweight="bold", fontsize=10.2)
e.set_xlabel("control bandwidth  (motor slew rate)")
e.set_ylabel("steady-state tracking error")
e.set_ylim(-0.04, 0.72)
e.legend(fontsize=8.4, loc="upper right")
e.grid(alpha=0.25)

# ---- E4b: latency / horizon frontier ----
f = ax[1, 1]
hz = e4["E4b_horizon_curve"]
sp = [x["speed"] for x in hz]
f.plot(sp, [x["err"] for x in hz], marker="o", lw=2.8, color=ORANGE)
f.axvline(1.0, ls="--", color=GREEN, lw=1.8, label="matched horizon (delay×speed=1)")
f.axhline(0.1, ls=":", color="#a33", lw=1.2, label="track / break")
f.set_title("E4b — latency / horizon frontier  [V band]\n"
            "(+1 predictor matches speed=1; off-nominal over/under-anticipates)",
            fontweight="bold", fontsize=10.2)
f.set_xlabel("target speed  (places / tick)")
f.set_ylabel("steady-state tracking error")
f.set_ylim(-0.04, 1.06)
f.legend(fontsize=8.2, loc="center right")
f.grid(alpha=0.25)

# ---- E5a: Shannon per-channel cap (effective bits vs requested) ----
g = ax[1, 2]
scols = {0: BLUE, 1: GREEN, 2: RED}
for i, row in enumerate(e5a["shannon_curve"]):
    req = [np.log2(c["requested_levels"]) for c in row["curve"]]
    eff = [c["effective_bits"] for c in row["curve"]]
    g.plot(req, eff, marker="o", lw=2.6, color=scols.get(i, "#555"),
           label=f"σ={row['sigma']} (ceiling {row['effective_bits_ceiling']:.1f} b)")
lim = max(np.log2(c["requested_levels"]) for c in e5a["shannon_curve"][0]["curve"])
g.plot([0, lim], [0, lim], ls=":", color="#999", lw=1.4, label="ideal (no noise: bits=request)")
g.set_title(f"E5a — single-channel bit depth is Shannon-capped  {h['grade_E5a_shannon_cap']}\n"
            "(effective bits saturate; ceiling ∝ SNR — the 'other side of the coin')",
            fontweight="bold", fontsize=10.2)
g.set_xlabel("requested bits per channel  (log₂ levels)")
g.set_ylabel("effective distinguishable bits")
g.legend(fontsize=8.0, loc="upper left")
g.grid(alpha=0.25)

# ---- E5b: hybrid exact-arithmetic hand-off ----
k = ax[1, 3]
cc = e5b["count_curve"]
Ks = [x["K"] for x in cc]
k.plot(Ks, [x["analog_exact_acc"] for x in cc], marker="o", lw=2.8, color=RED,
       label="analog accumulator (drifts)")
k.plot(Ks, [x["digital_exact_acc"] for x in cc], marker="s", lw=2.6, color=GREEN,
       label="digital register (exact)")
k.set_title(f"E5b — exact arithmetic needs a digital hand-off  {h['grade_E5b_hybrid_handoff']}\n"
            "(the hybrid: leave the analog domain only where exactness is required)",
            fontweight="bold", fontsize=10.2)
k.set_xlabel("stream length K  (number of increments)")
k.set_ylabel("exact-count accuracy")
k.set_ylim(0, 1.06)
k.legend(fontsize=8.4, loc="lower left")
k.grid(alpha=0.25)

fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig("wave_embodiment_atlas.png", dpi=125)
print("wrote wave_embodiment_atlas.png")
