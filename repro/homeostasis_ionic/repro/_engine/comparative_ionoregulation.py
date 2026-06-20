"""
comparative_ionoregulation.py  --  REMEDIATION module (v0.5.0, FIRST increment).

Closes the LARGEST gap found in the v0.4.0 audit: every prior object in this volume modeled
ONE species (human / mammalian mineral-acid-base-electrolyte homeostasis). The audit question
"which animals use ions precisely, which do not, and how are they distinguished?" had NO answer
because the package had no cross-species axis at all.

This module supplies that axis WITHOUT new tuning: it reuses the volume's OWN closed-loop control
law (vp_loops.ou_setpoint, whose deterministic step error is load/k) to separate osmotic STRATEGIES
on the SAME R19 substrate. The single control knob is the loop gain k -- how strongly the internal
milieu is DEFENDED against an external salinity load:

    high k  ->  regulator : internal state is held, environment is REJECTED   (precise ion user)
    low  k  ->  conformer : internal state TRACKS the environment              (non-regulator)

The premise -- WHICH clade uses WHICH strategy and the qualitative gain ordering -- is CITED
comparative physiology [L]. The reproduced result is the DIRECTION / ORDERING [V]: conformers track,
regulators defend, and the internal excursion under a salinity load is monotone in k. Absolute loop
gains and tolerated salinity ranges are [O]; per-species master-gene gamma is NOT yet measured, so
grounding each k in a measured gamma (as the human axis already does, kidney SIX2 gamma=1.5556 ->
k_terrestrial top of the ladder) is the next-task obstacle [O]/[H].

GRADES (C3): strategy assignment + gain ordering cited [L]; conformer-tracks / regulator-defends and
the monotone separation [V]; absolute k & salinity-tolerance magnitudes [O]; per-species gamma [O]/[H].

DETERMINISM: pure function of the cited STRATEGIES table + the volume's OU law; seeded; round-before-
return; two runs -> identical sha. This module is ADDITIVE -- it is not imported by the research gate
(gamma-emergence + stress battery), so the research sha is unchanged.
"""
import os, sys, math, json, hashlib

sys.path.insert(0, os.path.dirname(__file__))
import importlib
loops = importlib.import_module("vp_loops")


# ---------------------------------------------------------------------------
# Osmotic strategies across the animal kingdom (CITED comparative physiology [L]).
# k = closed-loop gain defending the internal milieu against the salinity load.
# The ORDERING (conformer < hybrid < aquatic regulator < terrestrial regulator) is the
# cited qualitative fact; the absolute k values are [O] placeholders that reproduce the ordering.
# ---------------------------------------------------------------------------
STRATEGIES = [
    # (name,                         k,   clade / exemplar,                                          mechanism note,                                                   ref)
    ("osmoconformer",               1.0, "most marine invertebrates (mussel, sea star, jellyfish)", "body fluid ~ seawater; internal osmolality TRACKS the environment ~1:1", "Willmer/Stone/Johnston 2005; Schmidt-Nielsen 1997"),
    ("urea-retaining elasmobranch", 2.0, "marine sharks & rays",                                    "osmoCONFORMS via urea+TMAO but IONO-regulates inorganic Na/Cl",     "Ballantyne 1997; Hammerschlag 2006"),
    ("hyperosmotic regulator",      3.0, "freshwater teleosts & amphibians",                        "gill/skin active uptake; dilute urine; internal > environment",    "Evans/Piermarini/Choe 2005"),
    ("hypoosmotic regulator",       3.0, "marine teleosts",                                         "gill ionocyte secretion; drink + scant urine; internal < env.",    "Evans/Piermarini/Choe 2005"),
    ("terrestrial regulator",       4.0, "mammals incl. human (this volume's baseline)",            "tight multi-loop defense (PTH/vitD/kidney/Na-K) -- baseline model", "Boron & Boulpaep, Medical Physiology"),
]

# Environmental salinity samples (dimensionless load, in units of the baseline disturbance) used to
# probe how much the internal milieu moves across a range of environments.
_ENV_LOADS = [0.5, 1.0, 1.5, 2.0]


def _internal_offset(k, load):
    """Deterministic steady internal displacement under an external salinity load.
    OU step error = load/k (sigma=0): conformer (low k) is dragged far; regulator (high k) holds."""
    return loops.ou_setpoint(k, sigma=0.0, load=load)["mean_offset"]


def strategy_separation(load=1.0):
    """Internal displacement and environment-tracking slope (d internal / d load = 1/k) per strategy."""
    rows = []
    for name, k, clade, mech, ref in STRATEGIES:
        rows.append(dict(strategy=name, k=k, clade=clade, mechanism=mech, ref=ref,
                         internal_offset=round(_internal_offset(k, load), 5),
                         tracking_slope=round(1.0 / k, 5)))
    return rows


def environment_sweep():
    """Across a range of environmental salinities, how wide does each strategy's internal state swing?
    Conformer swings nearly as much as the environment; regulator stays nearly flat (the precise user)."""
    rows = []
    for name, k, clade, mech, ref in STRATEGIES:
        internals = [round(_internal_offset(k, L), 5) for L in _ENV_LOADS]
        swing = round(max(internals) - min(internals), 5)            # internal range over the environment range
        env_range = round(max(_ENV_LOADS) - min(_ENV_LOADS), 5)      # the external range probed
        rows.append(dict(strategy=name, k=k, internal_states=internals,
                         internal_swing=swing, environmental_range=env_range,
                         fraction_of_environment_tracked=round(swing / env_range, 5)))
    return rows


def status():
    """Frontier-style honest status for the comparative axis."""
    loops.seed_everything()
    sep = strategy_separation()
    swp = environment_sweep()

    conformer = sep[0]
    terrestrial = sep[-1]
    ks = [r["k"] for r in sep]
    offs = [r["internal_offset"] for r in sep]

    # (1) the conformer's internal milieu tracks the environment more than the regulator's
    conformer_tracks = conformer["internal_offset"] > terrestrial["internal_offset"]
    # (2) internal excursion is monotone in loop gain (sort by k, offset must not increase)
    bym = sorted(zip(ks, offs))
    monotone = all(bym[i][1] >= bym[i + 1][1] - 1e-9 for i in range(len(bym) - 1))
    # (3) the terrestrial regulator holds tight against the salinity load
    regulator_defends = terrestrial["internal_offset"] < 0.5
    # (4) the tracking RATIO conformer/regulator equals the gain ratio k_reg/k_conf (load/k law)
    ratio = conformer["internal_offset"] / terrestrial["internal_offset"]
    predicted = terrestrial["k"] / conformer["k"]
    ratio_matches = abs(ratio - predicted) < 1e-3
    # (5) sweep: conformer tracks most of the environment, regulator tracks little
    conf_frac = swp[0]["fraction_of_environment_tracked"]
    reg_frac = swp[-1]["fraction_of_environment_tracked"]
    sweep_separates = conf_frac > reg_frac and reg_frac < 0.5

    demonstrations_pass = bool(conformer_tracks and monotone and regulator_defends
                               and ratio_matches and sweep_separates)

    return {
        "_what": "comparative ionoregulation: which animals defend ions vs conform to the environment, "
                 "on the SAME R19 substrate, via the volume's own OU loop-gain law (err=load/k)",
        "strategies": sep,
        "environment_sweep": swp,
        "conformer_internal_tracks_environment": bool(conformer_tracks),
        "internal_excursion_monotone_in_loop_gain": bool(monotone),
        "terrestrial_regulator_defends_setpoint": bool(regulator_defends),
        "tracking_ratio_conformer_over_regulator": round(ratio, 3),
        "predicted_ratio_k_reg_over_k_conf": round(predicted, 3),
        "tracking_ratio_matches_gain_law": bool(ratio_matches),
        "sweep_conformer_fraction_tracked": conf_frac,
        "sweep_regulator_fraction_tracked": reg_frac,
        "sweep_separates_regulator_from_conformer": bool(sweep_separates),
        "demonstrations_pass": demonstrations_pass,
        "grade": "[L] strategy assignment + gain ordering (cited comparative physiology); "
                 "[V] conformer-tracks / regulator-defends, monotone separation, ratio=gain law; "
                 "[O] absolute k & salinity tolerance; [O]/[H] per-species master-gene gamma not yet measured",
    }


if __name__ == "__main__":
    s = json.dumps(status(), sort_keys=True)
    print(json.dumps(status(), indent=1))
    print("sha:", hashlib.sha256(s.encode()).hexdigest()[:12])
