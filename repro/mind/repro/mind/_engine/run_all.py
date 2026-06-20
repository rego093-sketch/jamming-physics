#!/usr/bin/env python3
"""
mind EMERGENCE DRIVER  (self-contained, offline, deterministic)
===============================================================
Runs the in-package emergence engine end-to-end and FREEZES its output. This is the
code that was missing from the old package: the numbers in docs/ are now produced
HERE, in-package, from first principles -- closing the C1 reproducibility gap.

What it emerges, in developmental order (see vp_mind_engine.py for the physics):

  M0  brain organs from 4D-DNA           (FOXG1/EN1/SIM1/LHX2 master genes -> R19 organs)
  M1  the EM brainwave                    (E/I populations -> LFP -> a real field at speed c)
  M2  hippocampal memory                  (engram bistables; Hebbian write; cue completion;
                                           theta-phase write/retrieve separation)
  M3  parallel gamma micro-eddies         (gamma -> ignitability; winner-take-MOST)
  M4  basal-ganglia selection             (one winner; control selects none)
  M5  the learned (dopamine-RPE) field    (reward shapes which eddies appear next)
  M6  the stream of thought               (serial selection bound in a theta frame)
  M7  the embodied loop / open problem    (arousal-recall coupling; honest negative on access)

Outputs (all under _engine/results/):
  mind_emergence_results.json   the full M0..M7 result tree
  regression_scalars.json       the mechanism invariants the harness asserts
  expected_sha256.json          frozen digests (written one level up, in _engine/)

Run:   python3 run_all.py        (from the _engine/ directory)
Exit 0 = results emerged and frozen.  Determinism is asserted by _verify/run_regression.py.
"""
import os, json, hashlib
import vp_mind_engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")
os.makedirs(OUT, exist_ok=True)


def _canon(obj):
    """Canonical JSON bytes: sorted keys, rounded floats (via the engine helper),
    so the digest is portable across machines/BLAS as long as the math agrees."""
    return json.dumps(E._round(obj), sort_keys=True,
                      separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main():
    R = E.emerge_all()
    S = E.regression_scalars(R)

    results_path = os.path.join(OUT, "mind_emergence_results.json")
    scalars_path = os.path.join(OUT, "regression_scalars.json")
    with open(results_path, "wb") as f:
        f.write(_canon(R))
    with open(scalars_path, "wb") as f:
        f.write(_canon(S))

    digests = {
        "mind_emergence_results.json": hashlib.sha256(_canon(R)).hexdigest(),
        "regression_scalars.json": hashlib.sha256(_canon(S)).hexdigest(),
        "tree_sha256": E.sha256_of(R),
    }
    with open(os.path.join(HERE, "expected_sha256.json"), "w") as f:
        json.dump(digests, f, indent=2)

    print("emerged and froze:")
    print("  ", results_path)
    print("  ", scalars_path)
    print("  expected_sha256.json digests:")
    for k, v in digests.items():
        print(f"     {k:32s} {v}")
    # a compact human-readable headline
    print()
    print("HEADLINE (mechanism invariants):")
    print(f"   winner-take-most  soft={S['wtm_loser_soft']:.4f} > hard={S['wtm_loser_hard']:.4f}")
    print(f"   gamma->ignitability  r={S['ignitability_pearson']:.5f}  mono={S['ignitability_mono']}")
    print(f"   selection  winners={S['sel_nsel']}  control={S['sel_ctrl_nsel']}")
    print(f"   RPE  learned={S['rpe_target_learned']:.3f} > control={S['rpe_target_control']:.3f}")
    print(f"   memory  attractor={S['mem_attractor_overlap']:.2f}  "
          f"capacity/N={S['mem_capacity_per_N']:.3f}  theta-protects={bool(S['mem_phase_protects'])}")
    print(f"   EM brainwave  front_speed/c={S['em_front_speed_over_c']:.3f}")
    print(f"   field coherence across brain={S['field_coherence_across_brain']:.4f}  "
          f"(brain={S['field_brain_in_wavelengths']:.2e} wavelengths; "
          f"quantum shortfall={S['field_quantum_shortfall']:.1e}; efficacy=OPEN)")


if __name__ == "__main__":
    main()
