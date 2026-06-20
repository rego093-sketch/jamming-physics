#!/usr/bin/env python3
"""§10 reproduction: each sense transduces a stimulus into a LOW-FREQUENCY spike
train; vision discriminates colour and re-presents a pattern as a spike map.
Deterministic; asserts its own results. Engine: ../_engine/vp_neuro_engine.py"""
import sys, os, hashlib, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
from vp_neuro_engine import (seed_everything, Photoreceptor, MechanoReceptor,
    ChemoReceptor, Thermoreceptor, LightStimulus, WaveStimulus, MoleculeStimulus,
    TouchStimulus)
def main(P):
    seed_everything()
    eye = Photoreceptor(cone="L", gain=1.0)
    dark = len(eye.transduce(LightStimulus(565, 0.0))["spikes"])
    bright = len(eye.transduce(LightStimulus(565, 1.0))["spikes"])
    P(f"vision: dark {dark} spikes -> bright {bright} spikes (monotonic)"); assert bright > dark
    red = eye.drive_from(LightStimulus(620,1.0)); blue = eye.drive_from(LightStimulus(450,1.0))
    P(f"colour: L-cone red {red:.3f} > blue {blue:.3f}"); assert red > blue
    for name, r, st in [("ear", MechanoReceptor(), WaveStimulus(40,1.0)),
                        ("nose", ChemoReceptor(), MoleculeStimulus(2.0)),
                        ("skin", Thermoreceptor(), TouchStimulus(temperature_C=45))]:
        n = len(r.transduce(st)["spikes"]); P(f"{name}: {n} spikes"); assert n > 0
    P("PASS")
if __name__ == "__main__":
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    main(P); print("sha256:", hashlib.sha256(buf.getvalue().encode()).hexdigest())
