# §14 — Cerebellum → muscle, quantified (closes §8 open structure)

`motor_quantification.py` refines the motor output of §8: the size-principle recruitment
ORDER (DERIVED from Ohm's law, rheobase = dVth / R_input), the force-frequency MONOTONE rise
toward the twitch→tetanus ratio (a locked measured input, ~3.9×; the precise value is
muscle/species-dependent and stays `[O]`), the dual code, the stretch-reflex NEGATIVE-feedback
rejection ×(1+gain), and the cerebellar supervised error-decay + after-effect SIGN — orders,
shapes and signs forced `[F]` and verified `[V]`. Absolute gains/latencies/counts/ratios stay `[O]`.

## Recruitment is bound to two cited measured datasets

The size principle is not asserted; it is derived from Ohm's law and bound to measured cat
motoneuron data locked in `inputs/motoneuron_properties.json` (self-verifying `payload_sha256`):

- **Fleshman, Munson, Sypert & Friedman (1981)** *J Neurophysiol* 46:1326–1338
  (doi:10.1152/jn.1981.46.6.1326) — cat medial-gastrocnemius motoneuron pool spans input
  resistance 0.8–5.1 MΩ and rheobase 0.8–17.1 nA.
- **Gustafsson & Pinter (1984)** *J Physiol* 357:453–483 (doi:10.1113/jphysiol.1984.sp015511)
  — rheobase is strongly correlated with input conductance, but the rheobase range exceeds the
  conductance range by ~2× because threshold depolarisation rises with rheobase.

From the measured resistance span, constant-threshold Ohm's law predicts a rheobase span of
×6.375. A single threshold depolarisation of 7.471 mV (the pool's geometric-mean cell, derived
not tuned) places the predicted rheobases at 1.465→9.339 nA — both INSIDE the measured 0.8–17.1
nA range, so the magnitude is validated by CONTAINMENT (§16-style), not by fitting a target. The
measured rheobase span (×21.375) EXCEEDS the conductance-only prediction by ×3.353; that span-
excess is the measured Gustafsson-&-Pinter signature that dVth rises with rheobase. The
recruitment ORDER and the containment are forced `[F]`/verified `[V]`; the dVth-vs-rheobase
drift and the absolute newton force scale stay `[O]`. No constant is tuned to hit a target nA.

Run: `python3 motor_quantification.py` (deterministic; prints a result-block sha256).
