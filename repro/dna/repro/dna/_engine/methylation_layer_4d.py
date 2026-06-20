#!/usr/bin/env python3
# =============================================================================
#  methylation_layer_4d.py
#  -- Workstream A: the ENVIRONMENT-WRITABLE methylation layer M on top of the
#     fixed material gamma. The worked answer to: "environment is reflected in DNA
#     structurally -- where is that variable, and how do we READ it?"
#
#  WHY THIS CASE EXISTS (the gap it closes):
#    The interpreter reduces each promoter to a single scalar gamma = mean(-NN dG)
#    (~GC within a catalog). It COMPUTES cpg_density/atrun and then DISCARDS them;
#    methylation/motif reading is absent. But the layer where ENVIRONMENT writes onto
#    DNA -- reversibly, at specific CpG positions -- is the CpG methylation substrate,
#    which is ~orthogonal to gamma (1차 조사: corr(CpG O/E, gamma)=+0.42, R²18%).
#    The revised constitution (I3 design clause) DEMANDS that an environment-sensitive
#    trait state WHICH switch is built to be exposed to the drive, read from STRUCTURE
#    -- not asserted. This engine cashes that promissory note for the integument's
#    sister case: the lactase switch.
#
#  THE LACTASE CASE (measured, READ-ONLY; NCBI efetch GRCh38/GRCm39, 2026-06-15):
#    [F] SET conserved   : LCT present in human AND mouse (a conserved gene).
#    [F] gamma conserved  : |Δγ(LCT)| human-mouse = 0.034 < 0.05 (snake-ZRS "same
#                          material" scale) -> lactase PERSISTENCE/non-persistence is
#                          NOT a difference in the LCT material (gamma). Same as the
#                          snake-limb / human-hair logic.
#    [F] methylation substrate, read from STRUCTURE: the LCT regulatory region carries
#                          a LOCAL CpG hotspot (O/E_localmax 0.78, 2.3x the 2.5kb mean
#                          0.34 that a single scalar erases), retained ~1.8x more than
#                          mouse -> a methylation-TUNABLE switch EXISTS at the locus.
#                          THIS is the "designed exposure to the drive," read not asserted.
#    [F] direction        : age/diet drive methylation accumulation on that substrate ->
#                          the LCT switch is silenced; the persistence cis variant
#                          (MCM6 -13910 cluster) REDUCES that sensitivity.
#
#  THE M-LAYER (the addition): gamma stays read-only (Invariant I1/I2). A dynamic,
#  reversible variable M is seeded by the sequence methylation potential m0 and driven
#  by age/environment; it lowers the switch's effective drive h_eff = h_base - lam*M.
#  Once h_eff crosses the gamma-set spinodal the LCT state flips OFF DISCONTINUOUSLY
#  (R19 bistable). SAME gamma, two M-trajectories (genotype) -> opposite outcomes:
#  gamma alone CANNOT tell persistence from non-persistence; the M-layer can.
#
#  *** HONEST BOUNDARY (Layer-2 [O], with reasons -- see IRREPRODUCIBILITY_LEDGER):
#      absolute methylation level (beta), absolute age-of-silencing, and the rate
#      magnitudes (kappa, lam, h_base) are NOT computed -- they need external WGBS/array
#      data and calibration, not sequence. What is [F] is WHICH switch, same-material,
#      the methylation SUBSTRATE read from structure, and the DIRECTION. Determinism:
#      fixed gamma, bit-for-bit. NOT a clinical model. The "drink-milk-and-adapt"
#      plasticity is DOMINANTLY gut-microbiome/physiology -- ABOVE the DNA layer -- and
#      is explicitly outside this model (only the methylation-reversibility part is shown).
# =============================================================================
import os, sys, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from organism import core   # R19 substrate: settle / spinodal / sdot (gamma read-only)

DATA = os.path.join(HERE, "data", "lactase_interpretation.json")
FIG = os.path.join(HERE, "methylation_layer_4d.png")
RESULTS = os.path.join(HERE, "methylation_layer_results.json")

SAME_MATERIAL = 0.05      # snake-ZRS "same gamma" scale (whitepaper §4); our yardstick

# ---- Layer-2 [O] illustrative knobs (NOT sequence; documented DIRECTION only) -------
H_BASE = 0.45             # infancy expression drive (LCT ON at birth)        [O]
LAM    = 1.5              # how strongly methylation lowers the switch drive  [O]
KAPPA_NP = 0.080          # age-methylation rate, NON-persistence (high)      [O] dir
KAPPA_LP = 0.008          # age-methylation rate, persistence -13910*T (low)  [O] dir
AGES = np.arange(0, 76)   # abstract life-units (years-like); absolute scale  [O]


def load():
    J = json.load(open(DATA))
    return J


def m_of_age(age, m0, kappa):
    """Methylation state: saturating accumulation toward the sequence-set substrate m0.
       m0 (capacity) is READ FROM STRUCTURE [F]; kappa (rate, genotype) is [O] direction."""
    return m0 * (1.0 - math.exp(-kappa * age))


def lct_state(age, g, m0, kappa):
    """LCT master R19 state at a given age under the methylation layer.
       h_eff = H_BASE - LAM*M(age); >0 = lactase ON, <0 = silenced (discontinuous)."""
    h_eff = H_BASE - LAM * m_of_age(age, m0, kappa)
    return core.settle(g, h_eff, +math.sqrt(g))   # start ON (infancy), let methylation tilt it


def main():
    print("=" * 86)
    print("METHYLATION LAYER (M) on fixed gamma -- the lactase switch, environment read from STRUCTURE")
    print("  gamma READ-ONLY; M seeded by measured CpG substrate; absolute beta/age = Layer-2 [O].")
    print("=" * 86)

    J = load()
    G = core.Gate()
    R = {"yardstick_same_material": SAME_MATERIAL,
         "knobs_layer2": {"H_BASE": H_BASE, "LAM": LAM, "KAPPA_NP": KAPPA_NP, "KAPPA_LP": KAPPA_LP}}

    g_h = J["LCT_human"]["material"]["gamma"]
    g_m = J["LCT_mouse"]["material"]["gamma"]
    m0_h = J["LCT_human"]["material"]["cpg_oe_local_max"]
    m0_m = J["LCT_mouse"]["material"]["cpg_oe_local_max"]
    oe_h_mean = J["LCT_human"]["material"]["cpg_oe"]
    spn = core.spinodal(g_h)

    # -----------------------------------------------------------------------
    # [F] (1) SET conserved: LCT present in human AND mouse
    # -----------------------------------------------------------------------
    print("\n--- [F] (1) SET: the lactase gene LCT is present in human AND mouse (conserved) ---")
    set_ok = ("LCT_human" in J) and ("LCT_mouse" in J)
    G.check(set_ok, "LCT (lactase master) is a conserved gene present in human and mouse",
            "humans are NOT missing lactase; persistence is a regulation question, not inventory")
    R["set_conserved"] = bool(set_ok)

    # -----------------------------------------------------------------------
    # [F] (2) gamma conserved: the difference is NOT in the LCT material
    # -----------------------------------------------------------------------
    print("\n--- [F] (2) MATERIAL: LCT gamma is conserved human<->mouse (same material) ---")
    dg = abs(g_h - g_m)
    print(f"    LCT gamma  human={g_h:.4f}  mouse={g_m:.4f}  |Δγ|={dg:.4f}  (same-material scale {SAME_MATERIAL})")
    G.check(dg < SAME_MATERIAL,
            "LCT gamma is conserved human<->mouse -> persistence is NOT a material (gamma) difference",
            f"|Δγ|={dg:.4f} < {SAME_MATERIAL}; difference is forced into the regulatory layer (cis + methylation)")
    R["material_conserved"] = {"gamma_human": g_h, "gamma_mouse": g_m, "abs_dgamma": round(dg, 4)}

    # -----------------------------------------------------------------------
    # [F] (3) methylation SUBSTRATE read from STRUCTURE (the designed exposure)
    #         -- a LOCAL CpG hotspot the single-scalar mean erases; human > mouse
    # -----------------------------------------------------------------------
    print("\n--- [F] (3) EXPOSURE: a methylation substrate is READ from structure (not asserted) ---")
    print(f"    LCT human: 2.5kb mean CpG O/E={oe_h_mean:.3f}  BUT local-max O/E={m0_h:.3f}  "
          f"({m0_h/oe_h_mean:.1f}x the mean -> the scalar HIDES the hotspot)")
    print(f"    cross-species substrate: human local-max {m0_h:.3f} vs mouse {m0_m:.3f}  "
          f"({m0_h/m0_m:.1f}x more in human)")
    substrate_ok = (m0_h > 1.5 * oe_h_mean) and (m0_h > m0_m)
    G.check(substrate_ok,
            "a methylation-tunable substrate exists at the LCT locus, read from sequence structure [F]",
            "the single-scalar gamma erases a local CpG hotspot that IS the designed exposure to the drive")
    R["methylation_substrate"] = {"oe_mean_human": oe_h_mean, "oe_localmax_human": m0_h,
                                  "oe_localmax_mouse": m0_m, "hotspot_over_mean": round(m0_h/oe_h_mean, 2),
                                  "human_over_mouse": round(m0_h/m0_m, 2)}

    # -----------------------------------------------------------------------
    # [F] (4) THE M-LAYER: same gamma, two methylation trajectories -> opposite STATE
    #         and the flip is DISCONTINUOUS (R19 bistable)
    # -----------------------------------------------------------------------
    print("\n--- [F] (4) M-LAYER: same LCT gamma, genotype sets methylation rate -> opposite outcome ---")
    st_np = np.array([lct_state(a, g_h, m0_h, KAPPA_NP) for a in AGES])   # non-persistence
    st_lp = np.array([lct_state(a, g_h, m0_h, KAPPA_LP) for a in AGES])   # persistence -13910*T
    # age at which non-persistence flips OFF (state crosses 0), if any
    flip_idx = np.argmax(st_np < 0) if (st_np < 0).any() else None
    flip_age = int(AGES[flip_idx]) if flip_idx is not None else None
    np_silences = bool((st_np < 0).any())
    lp_stays_on = bool((st_lp > 0).all())
    # discontinuity: state drop across the flip (R19 bistable -> ~2*sqrt(g), not gradual)
    if flip_idx is not None and flip_idx > 0:
        jump = float(st_np[flip_idx-1] - st_np[flip_idx])
    else:
        jump = 0.0
    print(f"    non-persistence (kappa={KAPPA_NP}): LCT SILENCES with age  -> flips OFF ~age {flip_age} "
          f"[O]; discontinuous drop Δs={jump:.2f}")
    print(f"    persistence -13910*T (kappa={KAPPA_LP}): LCT STAYS ON across the span (lower methylation rate)")
    print(f"    SAME gamma ({g_h:.4f}) in both -> gamma is BLIND to the difference; the M-layer resolves it.")
    G.check(np_silences and lp_stays_on,
            "same LCT gamma, two methylation trajectories -> opposite STATE (gamma-blind, M-resolved) [F]",
            f"non-persistence silences (~age {flip_age} [O]); persistence holds ON; flip is discontinuous Δs={jump:.2f}")
    G.check(jump > 1.0,
            "the lactase silencing is a DISCONTINUOUS R19 flip, not a gradual fade [F]",
            f"state drop Δs={jump:.2f} (~2*sqrt(gamma)); no half-silenced lactase state")
    R["m_layer"] = {"nonpersistence_silences": np_silences, "persistence_stays_on": lp_stays_on,
                    "flip_age_OPEN": flip_age, "discontinuous_jump": round(jump, 3),
                    "same_gamma_both": g_h}

    # -----------------------------------------------------------------------
    # [F] (5) the DNA silencing is HYSTERETIC -- and that MATCHES the biology:
    #         lactase is not re-inducible, so the 'adapt by drinking' the question
    #         asks about must live in a layer ABOVE the DNA switch (it does: microbiome)
    # -----------------------------------------------------------------------
    print("\n--- [F] (5) hysteresis: once methylation silences LCT, lowering it does NOT restore it ---")
    silenced_state = lct_state(60, g_h, m0_h, KAPPA_NP)            # silenced at age 60 (non-persistence)
    # 'training' = sustained lactose relaxes the methylation tilt toward a LOWER M -> re-settle
    M_relaxed = 0.20 * m0_h                                       # sustained-exposure lower methylation [O]
    h_recover = H_BASE - LAM * M_relaxed
    recovered_state = core.settle(g_h, h_recover, silenced_state)
    # the switch does NOT flip back ON because the baseline drive H_BASE is itself sub-spinodal:
    irreversible = bool(silenced_state < 0 and recovered_state < 0)
    print(f"    silenced state(age60)={silenced_state:+.2f}  ->  relax methylation, re-settle={recovered_state:+.2f}")
    print(f"    H_BASE={H_BASE} < spinodal={spn:.2f}: the OFF state HOLDS -> silencing is HYSTERETIC (one-way).")
    print(f"    ★ This MATCHES the biology: human lactase is NOT re-inducible. So the 'drink milk and")
    print(f"      adapt' the question asks about is NOT lactase coming back -- it is a layer ABOVE the")
    print(f"      DNA switch (colonic microbiome + physiological tolerance), which is OUTSIDE this model. ★")
    print(f"    (Workstream C hook: the SAME machinery is TRAINABLE/reversible for a trait whose baseline")
    print(f"     drive clears the spinodal -- fixed vs trainable = sub- vs supra-spinodal H_BASE.)")
    G.check(irreversible,
            "DNA-methylation silencing of LCT is HYSTERETIC (one-way) -- matches lactase non-re-inducibility [F]",
            "the observed 'adapt by drinking' must be ABOVE the DNA layer (microbiome), outside this model [O]")
    R["hysteresis"] = {"silenced_state": round(silenced_state, 3), "after_relax_state": round(recovered_state, 3),
                       "irreversible_at_dna_layer": irreversible, "H_BASE": H_BASE, "spinodal": round(spn, 4),
                       "scope_note": "real lactose-tolerance adaptation is gut-microbiome/physiology, ABOVE the DNA layer [O]",
                       "fixed_vs_trainable": "fixed = sub-spinodal baseline (LCT); trainable = supra-spinodal baseline (Workstream C)"}

    # -----------------------------------------------------------------------
    # determinism (Invariant I2)
    # -----------------------------------------------------------------------
    J2 = load()
    fixed = abs(J2["LCT_human"]["material"]["gamma"] - g_h) < 1e-12
    G.check(fixed, "gamma is bit-identical on re-read (DNA read-only, Invariant I1/I2)", f"fixed={fixed}")

    # -----------------------------------------------------------------------
    # Layer-2 [O] register with reasons (Constitution C3)
    # -----------------------------------------------------------------------
    R["open_layer2"] = {
        "absolute_methylation_beta": "Layer-2 [O] -- needs WGBS/array data; NOT derivable from sequence",
        "absolute_age_of_silencing": "Layer-2 [O] -- calibration, not derived (flip_age is illustrative)",
        "rate_magnitudes_kappa_lam_hbase": "Layer-2 [O] -- documented DIRECTION only; magnitudes illustrative",
        "lactose_tolerance_training": "Layer-2 [O] -- dominantly gut-microbiome/physiology, ABOVE the DNA layer",
    }
    R["gates_pass"] = G.all_pass()
    json.dump(R, open(RESULTS, "w"), indent=2, ensure_ascii=False)

    print("\n" + "=" * 86)
    print(f"  ALL GATES: {'PASS' if G.all_pass() else 'FAIL'}   ·   LCT gamma conserved; methylation substrate")
    print("  read from structure; same gamma + two methylation trajectories -> opposite lactase STATE.")
    print("  ★ The environment-writable layer M is read from the CpG substrate (a Layer-1 design fact),")
    print("    NOT punted to 'Layer-2, unexplained.' Absolute beta/age stay [O]. Determinism: fixed gamma. ★")
    print("=" * 86)

    _figure(R, J, g_h, m0_h, st_np, st_lp, flip_age)
    return R


def _figure(R, J, g, m0, st_np, st_lp, flip_age):
    fig, ax = plt.subplots(1, 2, figsize=(13.2, 5.0))
    fig.suptitle("Methylation layer M on fixed gamma -- the lactase switch (environment read from structure)  ·  "
                 "same gamma, two methylation trajectories -> opposite STATE  ·  absolute beta/age = Layer-2 [O]",
                 fontsize=9.8)
    spn = core.spinodal(g)
    # (A) the methylation drive across age, and the gamma-set spinodal threshold
    M_np = [m0 * (1 - math.exp(-R["knobs_layer2"]["KAPPA_NP"] * a)) for a in AGES]
    M_lp = [m0 * (1 - math.exp(-R["knobs_layer2"]["KAPPA_LP"] * a)) for a in AGES]
    heff_np = [R["knobs_layer2"]["H_BASE"] - R["knobs_layer2"]["LAM"] * m for m in M_np]
    heff_lp = [R["knobs_layer2"]["H_BASE"] - R["knobs_layer2"]["LAM"] * m for m in M_lp]
    ax[0].plot(AGES, heff_np, color="#c0392b", lw=2, label="non-persistence (high methylation rate)")
    ax[0].plot(AGES, heff_lp, color="#16a085", lw=2, label="persistence −13910*T (low rate)")
    ax[0].axhline(-spn, color="#333", ls="--", lw=1)
    ax[0].annotate(f"−spinodal = −{spn:.2f}  (γ-set OFF threshold)", (2, -spn), fontsize=8,
                   va="bottom", color="#333")
    if flip_age is not None:
        ax[0].axvline(flip_age, color="#c0392b", ls=":", lw=1)
        ax[0].annotate(f"silences ~age {flip_age} [O]", (flip_age, 0.2), fontsize=8, color="#c0392b",
                       rotation=90, va="bottom")
    ax[0].set_xlabel("age (abstract life-units; absolute = Layer-2 [O])")
    ax[0].set_ylabel("effective drive on LCT switch  h_eff = H_BASE − λ·M")
    ax[0].set_title("(A) methylation lowers the switch drive with age\nsame γ; genotype sets the rate (Layer-2)",
                    fontsize=9.5)
    ax[0].legend(fontsize=7.5, loc="upper right")
    # (B) the resulting LCT STATE -- discontinuous flip for non-persistence, ON for persistence
    ax[1].plot(AGES, st_np, color="#c0392b", lw=2, label="non-persistence → SILENCES")
    ax[1].plot(AGES, st_lp, color="#16a085", lw=2, label="persistence → stays ON")
    ax[1].axhline(0, color="k", lw=0.5)
    ax[1].fill_between(AGES, 0, 2, color="#eafaf1", zorder=0)
    ax[1].fill_between(AGES, -2, 0, color="#fdecea", zorder=0)
    ax[1].text(60, 1.1, "lactase ON", color="#16a085", fontsize=8.5, ha="center")
    ax[1].text(60, -1.1, "lactase OFF", color="#c0392b", fontsize=8.5, ha="center")
    ax[1].set_xlabel("age (abstract life-units; absolute = Layer-2 [O])")
    ax[1].set_ylabel("LCT master state  s   (>0 ON, <0 silenced)")
    ax[1].set_title(f"(B) SAME γ={g:.3f}: the M-layer resolves what γ cannot\nsilencing is a discontinuous R19 flip",
                    fontsize=9.5)
    ax[1].legend(fontsize=7.5, loc="center right")
    ax[1].set_ylim(-1.5, 1.5)
    plt.savefig(FIG, dpi=120, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
