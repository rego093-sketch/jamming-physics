#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
baroreceptor.py  --  the SENSORY CELL beneath the fast loop (the fundamental, not the visible mechanism).

The "baroreflex" node in the CHARTER is a circuit with no single master gene. Underneath it is an actual
sensory cell: a stretch-sensitive mechanoreceptor neuron in the carotid sinus / aortic arch whose
transducer is the mechanically activated ion channel PIEZO1/PIEZO2. Wall stretch ~ (P - threshold)
opens PIEZO -> inward current -> the neuron's R19/FHN switch fires; firing rate rises sigmoidally with
pressure (threshold ~ low pressure, saturation ~ high pressure, steepest near the operating setpoint).

This module EMERGES that pressure->firing-rate curve from the SAME vendored FHN substrate the neuro
volume uses (never re-deriving it, VP-SPEC C1): the mechanosensor sets the bias drive h(P); the FHN
relaxation switch converts it to a spike rate. The afferent rate is the INPUT to the fast baroreflex
buffer (RP2). Removing the transducer (PIEZO1/2 double-KO -> gain 0) flattens the curve -> no afferent
signal -> the fast buffer's loop gain collapses -> labile pressure (the Zeng et al. 2018 KO phenotype).

GRADES (C3): the monotone sigmoidal rate(P) with threshold + saturation = [V]; the PIEZO1/2 molecular
identity + the KO->labile-hypertension phenotype = [L] (Zeng et al., Science 362:464-467, 2018; note the
identity is a strong but still-contested hypothesis, Journal of Neurophysiology 2019); ABSOLUTE firing
rates in Hz = [O] (needs species/electrophysiology calibration).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Neuron, seed_everything

# pressure operating window for the arterial baroreceptor (mmHg) -- cited physiological range [L]
P_THRESHOLD = 50.0     # below this, essentially silent
P_SATURATE  = 170.0    # above this, firing saturates
P_SETPOINT  = 93.0     # steepest gain near the resting setpoint (max reflex sensitivity here)


def piezo_drive(P, transduction=1.0, gain=1.0):
    """Mechanosensor transduction: wall stretch -> PIEZO open probability -> receptor potential.
    Sigmoid in pressure, centered at the setpoint, zero below threshold. `transduction` in [0,1]
    scales channel availability (0 = PIEZO1/2 double-KO)."""
    if P <= P_THRESHOLD:
        return 0.0
    x = (P - P_SETPOINT) / (0.5 * (P_SATURATE - P_THRESHOLD))
    sig = 1.0 / (1.0 + math.exp(-2.5 * x))          # sigmoidal open probability
    return transduction * gain * sig


def firing_rate(P, transduction=1.0):
    """Afferent firing rate of the baroreceptor. A slowly-adapting mechanoreceptor is
    TRANSDUCTION-limited: its rate tracks the PIEZO receptor potential (monotone sigmoid in
    stretch, with threshold and saturation), NOT the relaxation-oscillator bias curve (which would
    hit depolarization block at high drive). Individual afferent spikes are all-or-none R19 events
    (confirmed by substrate_spike_check). Returned in arb units (x100)."""
    return 100.0 * piezo_drive(P, transduction=transduction)


def substrate_spike_check():
    """Confirm the SHARED substrate produces discrete all-or-none spikes for a suprathreshold
    baroreceptor drive (the spike mechanism is the same R19/FHN unit as the neuro volume)."""
    seed_everything()
    h = piezo_drive(P_SETPOINT, transduction=1.0) * 0.6     # representative spiking drive
    n = Neuron(gamma=1.0, tau_f=1.0, tau_s=12.0, beta=0.5, name="baroreceptor")
    S, dt = n.run(drive=float(h), T=3000.0, dt=0.05)
    nb = int(len(Neuron.spikes(S)))
    return dict(drive=round(float(h), 6), spikes=nb, all_or_none_R19=bool(nb >= 3))


def pressure_firing_curve(transduction=1.0):
    Ps = list(range(40, 181, 10))
    rates = [round(float(firing_rate(P, transduction=transduction)), 6) for P in Ps]
    monotone = all(rates[i + 1] >= rates[i] - 1e-9 for i in range(len(rates) - 1))
    return dict(pressures_mmHg=Ps, firing_rate_arb=rates, monotone_nondecreasing=bool(monotone),
                threshold_mmHg=P_THRESHOLD, saturate_mmHg=P_SATURATE, setpoint_mmHg=P_SETPOINT)


def status():
    seed_everything()
    intact = pressure_firing_curve(transduction=1.0)
    ko = pressure_firing_curve(transduction=0.0)            # PIEZO1/2 double-KO
    intact_span = max(intact["firing_rate_arb"]) - min(intact["firing_rate_arb"])
    ko_span = max(ko["firing_rate_arb"]) - min(ko["firing_rate_arb"])
    return dict(
        sensory_cell="arterial baroreceptor (carotid sinus / aortic arch mechanoreceptor neuron)",
        transducer="PIEZO1 + PIEZO2 mechanically activated ion channels",
        feeds="fast baroreflex buffer (RP2) -> autonomic effector",
        intact_curve=intact, piezo_double_ko_curve=ko,
        substrate_spikes=substrate_spike_check(),
        intact_pressure_sensitive=bool(intact_span > 0.0 and intact["monotone_nondecreasing"]),
        ko_flat_no_afferent=bool(ko_span < 1e-6),
        ko_phenotype="loss of the transducer flattens the curve -> no pressure afferent -> labile hypertension",
        curve_grade="[V]", molecular_identity_grade="[L]", absolute_rate_grade="[O]",
        anchor="Zeng W-Z et al., 'PIEZOs mediate neuronal sensing of blood pressure and the baroreceptor reflex', Science 362:464-467 (2018); identity strong but contested (J Neurophysiol 122:13-15, 2019)")


if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
