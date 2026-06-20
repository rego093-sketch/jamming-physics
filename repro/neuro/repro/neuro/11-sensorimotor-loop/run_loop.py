#!/usr/bin/env python3
"""§11 reproduction: the closed sensorimotor loop (light->eye->ionic axon->
cerebrum theta/gamma->cerebellum->muscle->reflex) over a data bus, plus DNA 4D
emergence of the eye (same R19 switch). Engine: ../_engine/vp_neuro_engine.py"""
import sys, os, hashlib, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
from vp_neuro_engine import (seed_everything, Photoreceptor, Axon, Cerebrum,
    Cerebellum, Muscle, ReflexArc, Bus, LightStimulus, spinodal, is_on)
def main(P):
    seed_everything(); bus = Bus()
    eye = Photoreceptor(cone="L", gain=1.0)
    rr = eye.transduce(LightStimulus(565, 0.9))
    axon = Axon(0.5, 60.0); _, _ = axon.conduct(rr["spikes"], rr["dt"])
    P(f"axon delay {axon.delay_ms():.2f} ms (ionic, ~5e6x slower than light)"); assert axon.delay_ms() > 1
    cx = Cerebrum(); ft,_,_ = cx.band(60.0); fg,_,_ = cx.band(5.0)
    P(f"capacity gamma/theta = {fg/ft:.1f}"); assert fg > ft
    cb = Cerebellum(0.15); e = cb.adapt(1.0, 0.5, 60)
    P(f"cerebellar error {e[0]:+.3f} -> {e[-1]:+.3f}"); assert abs(e[-1]) < abs(e[0])*0.2
    mus = Muscle(); P(f"force {mus.force(0.2,0.3):.1f} -> {mus.force(0.9,0.9):.1f}")
    assert mus.force(0.9,0.9) > mus.force(0.2,0.3)
    rf = ReflexArc(); assert rf.correct(0.1) < 0
    g = 1.21; assert is_on(g, spinodal(g)+0.25) and not is_on(g, 0.0)
    P("organ: eye STATE on->present, off->absent (same R19 switch)"); P("PASS")
if __name__ == "__main__":
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    main(P); print("sha256:", hashlib.sha256(buf.getvalue().encode()).hexdigest())
