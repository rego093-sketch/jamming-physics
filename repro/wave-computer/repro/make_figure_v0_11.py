#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the v0.11 atlas from wave_adapt_closure_results.json (POST-PROGRAM HARDENING:
re-probe the L9 A3 [O] — real-time adaptation — with the proven L5 dual store wired in,
and show the [O]->[V] closure INLINE on one paired battery). Four panels:
  P1  the closure: single store FAILS the full rule-switch, dual store recovers to band,
      across the shift sweep (the inherited A3 [O] reproduced, then closed).
  P2  the mechanism is the FAST store, not the normalization: dual-norm and dual-raw
      (unnormalized sum) BOTH beat single everywhere -> equal-vote is scale-equalizing only.
  P3  the closure is sign-stable across machine size (B x N).
  P4  the verdict: A3 [O]->[V], ladder 7/7 [V] with the dual store wired in (the S10 6/7
      single-store record stands as the minimal machine's honest limit); firewall intact.
FUNCTION only. No tuned constants. Fast store = inherited R3/C2, reused unchanged.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

r = json.load(open("wave_adapt_closure_results.json"))
T1, T2, H = r["T1_closure"], r["T2_size_robustness"], r["headline"]
BAND = T1["band"]

BLUE, GREEN, PURPLE, RED, ORANGE, GREY = \
    "#1f5fa6", "#1f7a3d", "#6a1b9a", "#c0392b", "#e08214", "#8a8a8a"

fig, ax = plt.subplots(2, 2, figsize=(15.2, 11.4))
fig.suptitle(
    "vp_wave_computer v0.11 — POST-PROGRAM HARDENING: the A3 [O]->[V] closure, INLINE\n"
    "re-probe the L9 lone open rung (real-time adaptation) with the proven L5 dual store wired in: "
    "single additive store FAILS a switched rule, the dual store CLOSES\n"
    "FIREWALL: a functional adaptation closure, the hard-problem blank stays OPEN  —  "
    "consciousness_claim=0, hard_problem_open=1, new_tuned_constants=0  ·  fast store = inherited R3/C2, reused unchanged",
    fontsize=10.6, fontweight="bold")

# ---------------------------------------------------------------- P1 the closure
a = ax[0, 0]
by = T1["by_shift"]
sf = [c["shift_frac"] for c in by]
post_single = [c["post_single"] for c in by]
post_dual = [c["post_dual_norm"] for c in by]
pre = [c["pre"] for c in by]
dip = [c["dip"] for c in by]
a.plot(sf, pre, "s--", color=GREY, lw=1.4, ms=5, alpha=0.7, label="pre-shift baseline")
a.plot(sf, dip, "v:", color=ORANGE, lw=1.6, ms=6, label="dip (immediately post-shift)")
a.plot(sf, post_single, "o-", color=RED, lw=2.4, ms=7, label="SINGLE store, post-recovery  [O]")
a.plot(sf, post_dual, "o-", color=GREEN, lw=2.4, ms=7, label="DUAL store, post-recovery  [V]")
a.axhline(BAND, color=PURPLE, ls="-.", lw=1.6, alpha=0.85, label=f"recovery band {BAND}")
a.set_title("P1 · the closure: single FAILS the switch, dual CLOSES\n"
            "post-shift recovery vs fraction of the cue battery re-mapped",
            fontsize=10, fontweight="bold")
a.set_xlabel("shift fraction (share of cues given a new response)")
a.set_ylabel("hetero-association recovery")
a.set_ylim(0.0, 1.06); a.set_xticks(sf)
a.legend(fontsize=7.8, loc="lower left"); a.grid(alpha=0.25)

# ---------------------------------------------------------------- P2 mechanism, not norm
a = ax[0, 1]
dual_norm = [c["post_dual_norm"] for c in by]
dual_raw = [c["post_dual_raw"] for c in by]
x = np.arange(len(sf)); w = 0.26
a.bar(x - w, post_single, w, color=RED, label="single store  [O]")
a.bar(x, dual_raw, w, color=BLUE, label="dual, RAW unnormalized sum")
a.bar(x + w, dual_norm, w, color=GREEN, label="dual, equal-vote (L2-norm) sum")
a.axhline(BAND, color=PURPLE, ls="-.", lw=1.6, alpha=0.85, label=f"band {BAND}")
a.set_title("P2 · the mechanism is the FAST store, not the normalization\n"
            "raw-sum dual ALSO beats single everywhere -> equal-vote is scale-equalizing only",
            fontsize=10, fontweight="bold")
a.set_xlabel("shift fraction"); a.set_ylabel("post-shift recovery")
a.set_xticks(x); a.set_xticklabels([f"{s:g}" for s in sf])
a.set_ylim(0.0, 1.06); a.legend(fontsize=7.8, loc="lower left"); a.grid(alpha=0.25, axis="y")

# ---------------------------------------------------------------- P3 size robustness
a = ax[1, 0]
cfgs = T2["by_config"]
labels = [f"B={c['B']}\nN={c['N']}" for c in cfgs]
xb = np.arange(len(cfgs)); w = 0.2

def at_shift(c, s):
    for e in c["by_shift"]:
        if abs(e["shift_frac"] - s) < 1e-9:
            return e
    return {"post_single": np.nan, "post_dual_norm": np.nan}

s_half = [at_shift(c, 0.5)["post_single"] for c in cfgs]
d_half = [at_shift(c, 0.5)["post_dual_norm"] for c in cfgs]
s_full = [at_shift(c, 1.0)["post_single"] for c in cfgs]
d_full = [at_shift(c, 1.0)["post_dual_norm"] for c in cfgs]
a.bar(xb - 1.5 * w, s_half, w, color=RED, alpha=0.6, label="single, sf=0.5")
a.bar(xb - 0.5 * w, d_half, w, color=GREEN, alpha=0.6, label="dual, sf=0.5")
a.bar(xb + 0.5 * w, s_full, w, color=RED, label="single, sf=1.0 (full switch)")
a.bar(xb + 1.5 * w, d_full, w, color=GREEN, label="dual, sf=1.0 (full switch)")
a.axhline(BAND, color=PURPLE, ls="-.", lw=1.6, alpha=0.85, label=f"band {BAND}")
a.set_title("P3 · the closure is sign-stable across machine size\n"
            "single fails the full switch, dual closes to band at every (B, N)",
            fontsize=10, fontweight="bold")
a.set_xlabel("machine size"); a.set_ylabel("post-shift recovery")
a.set_xticks(xb); a.set_xticklabels(labels, fontsize=8.5)
a.set_ylim(0.0, 1.06); a.legend(fontsize=7.6, loc="lower left"); a.grid(alpha=0.25, axis="y")

# ---------------------------------------------------------------- P4 verdict
a = ax[1, 1]; a.axis("off")
def ok(b): return "PASS" if b else "----"
lines = [
    ("THE A3 [O]->[V] CLOSURE  (post-program hardening)", "head"),
    ("", "sp"),
    ("the inherited shortfall (S10, L9 ladder):", "sub"),
    ("  A3 real-time adaptation was the LONE [O] — 6/7 rungs [V].", "txt"),
    ("  a single additive Hebbian store cannot OVER-WRITE a switched", "txt"),
    ("  rule: old + new associations superpose in ONE field, so the", "txt"),
    ("  clean-up settles on a blend and recovery falls below band.", "txt"),
    ("", "sp"),
    ("the fix — the proven L5 dual store, reused UNCHANGED:", "sub"),
    ("  slow additive store (full history)  +  FAST one-shot episodic", "txt"),
    ("  field over the current-rule snapshot (the inherited R3 / C2", "txt"),
    ("  _episodic_field = frozen-L0 hebbian_field). read = settle under", "txt"),
    ("  both fields, equal vote. the new rule lives in a SEPARATE field.", "txt"),
    ("", "sp"),
    (f"  [{ok(H['T1_single_fails_at_full_switch'])}]  single store FAILS the full rule-switch", "res"),
    (f"  [{ok(H['T1_dual_recovers_to_band_everywhere'])}]  dual store recovers to band at EVERY shift", "res"),
    (f"  [{ok(H['T1_dual_raw_unnormalized_also_beats_single'])}]  raw-sum dual also beats single (norm not load-bearing)", "res"),
    (f"  [{ok(H['T2_closure_sign_stable_across_size'])}]  closure sign-stable across machine size", "res"),
    ("", "sp"),
    (f"  A3 grade after the dual store:  {H['grade_A3_after_dual_store']}", "verdict"),
    ("  ladder: 7/7 [V] with the dual store wired in", "verdict"),
    ("  (S10 6/7 single-store [O] stands as the minimal", "txt"),
    ("   machine's honest limit — paired, not overwritten)", "txt"),
    ("", "sp"),
    ("FIREWALL  consciousness_claim=0  hard_problem_open=1", "fire"),
    ("NO-TUNING  new_tuned_constants=0", "fire"),
]
y = 1.0
for text, kind in lines:
    if kind == "sp":
        y -= 0.018; continue
    if kind == "head":
        a.text(0.0, y, text, fontsize=12, fontweight="bold", color=PURPLE, transform=a.transAxes)
    elif kind == "sub":
        a.text(0.0, y, text, fontsize=10, fontweight="bold", color=BLUE, transform=a.transAxes)
    elif kind == "res":
        a.text(0.0, y, text, fontsize=9.6, fontweight="bold", color=GREEN, family="monospace", transform=a.transAxes)
    elif kind == "verdict":
        a.text(0.0, y, text, fontsize=10.2, fontweight="bold", color=GREEN, transform=a.transAxes)
    elif kind == "fire":
        a.text(0.0, y, text, fontsize=9.4, fontweight="bold", color=RED, family="monospace", transform=a.transAxes)
    else:
        a.text(0.0, y, text, fontsize=9.2, color="#222222", transform=a.transAxes)
    y -= 0.041

fig.tight_layout(rect=[0, 0, 1, 0.945])
fig.savefig("wave_adapt_closure_atlas.png", dpi=130, bbox_inches="tight")
print("wrote wave_adapt_closure_atlas.png")
