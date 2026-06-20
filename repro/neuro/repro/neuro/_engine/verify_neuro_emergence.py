#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_neuro_emergence.py — runs every module, proves emergence happens, gates.

PART 1  sensory transduction  : each sense converts a stimulus into a LOW-FREQ
        spike train (eye/ear/nose/skin). A tiny retina shows how visual cells
        convert a pattern and "show" it as a spike image.
PART 2  closed sensorimotor loop : light -> eye -> ionic axon -> cerebrum (bands,
        θ/γ capacity) -> cerebellum (supervised error -> 0) -> muscle (force),
        with reflex feedback. Modules exchange data over the bus.
PART 3  DNA 4D organ emergence : the eye is EMERGED from measured-γ — the same
        R19 switch as the neuron. STATE on/off decides whether the eye forms
        ("parts present ≠ trait").

Deterministic: run twice, compare the result-block sha256.
"""
import sys, os, io, math, hashlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vp_neuro_engine import (
    seed_everything, spinodal, barrier, is_on,
    Neuron, dominant_freq,
    LightStimulus, WaveStimulus, MoleculeStimulus, TouchStimulus,
    Photoreceptor, MechanoReceptor, ChemoReceptor, Thermoreceptor,
    Axon, Cerebrum, Cerebellum, Muscle, ReflexArc, Bus,
)

def banner(P, t): P("\n" + "="*70); P(t); P("="*70)

def run_all(P):
    seed_everything()

    # ---------------- PART 1 : sensory transduction -> low frequency ----------
    banner(P, "PART 1 — SENSORY TRANSDUCTION (stimulus → low-frequency spikes)")

    # a neuron at rest: confirm it is a LOW-FREQUENCY relaxation oscillator
    base = Neuron(gamma=1.0)
    Sb, dtb = base.run(0.35, T=4000, dt=0.05)
    f_base = dominant_freq(Sb, dtb)
    P(f"[substrate] resting neuron dominant rhythm = {f_base*1000:.2f} mHz-scale "
      f"(slow relaxation oscillator)   [F]/[V]")
    assert f_base < 0.05, "neuron must be intrinsically LOW frequency"

    P("\n  sense        stimulus                     drive    spikes  rate(arb)")
    eye = Photoreceptor(cone="L", gain=1.0)
    r_dark = eye.transduce(LightStimulus(565, intensity=0.0))
    r_bright = eye.transduce(LightStimulus(565, intensity=1.0))
    P(f"  eye(L)       565nm  dark  I=0.0           {r_dark['drive']:+.3f}   "
      f"{len(r_dark['spikes']):5d}   {r_dark['rate_hz']*1000:7.2f}")
    P(f"  eye(L)       565nm  bright I=1.0          {r_bright['drive']:+.3f}   "
      f"{len(r_bright['spikes']):5d}   {r_bright['rate_hz']*1000:7.2f}")
    assert len(r_bright['spikes']) > len(r_dark['spikes']), \
        "a brighter visible light must produce MORE spikes"

    ear = MechanoReceptor(gain=1.0)
    r_ear = ear.transduce(WaveStimulus(40.0, amplitude=1.0))  # 40 Hz low tone
    P(f"  ear          40Hz tone  A=1.0             {r_ear['drive']:+.3f}   "
      f"{len(r_ear['spikes']):5d}   {r_ear['rate_hz']*1000:7.2f}")

    nose = ChemoReceptor(gain=1.0)
    r_nose = nose.transduce(MoleculeStimulus(2.0, kind="odor"))
    P(f"  nose         odorant c=2.0                {r_nose['drive']:+.3f}   "
      f"{len(r_nose['spikes']):5d}   {r_nose['rate_hz']*1000:7.2f}")

    skin = Thermoreceptor(gain=1.0)
    r_skin = skin.transduce(TouchStimulus(temperature_C=45.0))   # hot
    P(f"  skin(thermo) 45°C                         {r_skin['drive']:+.3f}   "
      f"{len(r_skin['spikes']):5d}   {r_skin['rate_hz']*1000:7.2f}")

    # colour discrimination: the L cone responds more to red than to blue  [V]
    red  = eye.drive_from(LightStimulus(620, 1.0))
    blue = eye.drive_from(LightStimulus(450, 1.0))
    P(f"\n  [colour] L-cone drive: red(620nm)={red:.3f} > blue(450nm)={blue:.3f}"
      f"  → wavelength is read as colour   [V]")
    assert red > blue

    # --- tiny RETINA: how visual cells convert a pattern and 'show' it --------
    P("\n  [retina] a 5×5 light pattern (a 'T') → per-pixel L-cone spike counts:")
    pattern = np.array([
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0]], float)
    spike_img = np.zeros_like(pattern)
    for i in range(5):
        for j in range(5):
            rr = eye.transduce(LightStimulus(565, intensity=float(pattern[i,j])),
                               T=600, dt=0.05)
            spike_img[i,j] = len(rr['spikes'])
    for row in spike_img:
        P("           " + " ".join(f"{int(v):2d}" for v in row))
    # the converted spike image must preserve the lit pixels (the 'T' shows)
    assert (spike_img[pattern>0].mean() > spike_img[pattern==0].mean()), \
        "the retina must reproduce the lit pattern in spike counts"
    P("           → lit pixels carry more spikes: the image is re-presented as a"
      " spike map (the 'T' is preserved).  [V]")

    # ---------------- PART 2 : closed sensorimotor loop -----------------------
    banner(P, "PART 2 — CLOSED SENSORIMOTOR LOOP (modules exchange data)")
    bus = Bus()

    # 1) stimulus -> eye
    light = LightStimulus(565, intensity=0.9)
    bus.send("stimulus", "eye", "light", dict(nm=565, I=0.9, angle=light.angle_deg()))
    rr = eye.transduce(light)
    bus.send("eye", "axon", "spikes", dict(n=len(rr['spikes']), rate=rr['rate_hz']))
    P(f"  stimulus→eye : 565nm I=0.9 (propagation angle χ={light.angle_deg():.3f}°)")
    P(f"  eye→axon     : {len(rr['spikes'])} spikes (ionic, NOT light)")

    # 2) ionic axon delay (guardrail: slow)
    axon = Axon(length_m=0.5, speed_mps=60.0)
    _, d = axon.conduct(rr['spikes'], rr['dt'])
    bus.send("axon", "cerebrum", "delayed-spikes", dict(delay_ms=axon.delay_ms()))
    P(f"  axon→cerebrum: conduction delay {axon.delay_ms():.2f} ms "
      f"(60 m/s ionic ≈ {3e8/60:.0e}× slower than light)")
    assert axon.delay_ms() > 1.0   # ms-scale, not light-speed

    # 3) cerebrum integrates -> band + percept; θ/γ capacity
    cx = Cerebrum(gamma=1.0)
    integ = cx.integrate(rr['rate_hz']*1000, tau_inh=20.0)
    f_theta, _, _ = cx.band(tau_inh=60.0)   # slow inhibition -> theta
    f_gamma, _, _ = cx.band(tau_inh=5.0)    # fast inhibition -> gamma
    cap = cx.working_memory_capacity(f_theta, f_gamma)
    bus.send("cerebrum", "cerebellum", "drive", dict(percept=integ['percept']))
    P(f"  cerebrum     : band walk θ={f_theta*1000:.2f} → γ={f_gamma*1000:.2f} "
      f"(arb), capacity γ/θ = {cap:.1f} slots  (θ/γ code, neuro 04)")
    assert f_gamma > f_theta, "faster inhibition must give a higher band"

    # 4) cerebellum learns the motor command (error -> 0), then after-effect
    cb = Cerebellum(lr=0.15)
    errs = cb.adapt(target=1.0, perturbation=0.5, trials=60)
    after, _ = cb.after_effect(target=1.0, trials=20)
    bus.send("cerebellum", "muscle", "command", dict(w=cb.w))
    P(f"  cerebellum   : motor error {errs[0]:+.3f} → {errs[-1]:+.3f} "
      f"(supervised, delta-rule); after-effect sign flips to {after[0]-1.0:+.3f}")
    assert abs(errs[-1]) < abs(errs[0]) * 0.2, "cerebellar error must shrink"

    # 5) muscle turns command into graded force
    mus = Muscle(n_units=20, tetanus_ratio=3.9)
    f_lo = mus.force(drive=0.2, rate_frac=0.3)
    f_hi = mus.force(drive=0.9, rate_frac=0.9)
    bus.send("muscle", "world", "force", dict(low=f_lo, high=f_hi))
    P(f"  muscle       : force low={f_lo:.2f} → high={f_hi:.2f} "
      f"(recruitment + force-frequency, twitch→tetanus 3.9×)")
    assert f_hi > f_lo

    # 6) reflex feedback closes the loop
    reflex = ReflexArc(gain=9.4)
    corr = reflex.correct(stretch=0.1)
    bus.send("muscle", "eye", "stretch-feedback", dict(correction=corr))
    P(f"  reflex       : stretch 0.10 → correction {corr:+.2f} (negative feedback, loop closed)")
    assert corr < 0

    P("\n  bus trace:")
    for s, arrow, d2, k in bus.trace():
        P(f"     {s:10s} {arrow} {d2:10s}  [{k}]")

    # ---------------- PART 3 : DNA 4D organ emergence -------------------------
    banner(P, "PART 3 — DNA 4D EMERGENCE OF THE EYE (same R19 switch)")
    # measured-γ stand-ins (Layer-1 [F] form; absolute is Layer-2 [O])
    PAX6 = 1.21   # eye master-control γ (read-only material constant, illustrative)
    sp = spinodal(PAX6)
    P(f"  eye master switch γ(PAX6)={PAX6}: spinodal |h_sp|={sp:.3f}, barrier={barrier(PAX6):.3f}")
    eye_on  = is_on(PAX6, h=sp + 0.25)   # master cis ON -> eye forms
    eye_off = is_on(PAX6, h=0.0)         # master cis OFF -> no eye (parts present ≠ trait)
    P(f"  STATE ON  (cis drive {sp+0.25:.2f}) → eye present? {eye_on}")
    P(f"  STATE OFF (cis drive 0.00)        → eye present? {eye_off}")
    assert eye_on and not eye_off, "γ sets threshold; STATE (on/off) decides the organ"
    P("  → the eye is EMERGED by the same R19 switch that makes the neuron fire;"
      " STATE, not γ, decides presence.  [F]")

    banner(P, "ALL EMERGENCE CHECKS PASSED — loop runs, organs emerge, guardrails held")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run_all(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()

if __name__ == "__main__":
    h = main()
    print("\nresult-block sha256:", h)
