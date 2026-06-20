#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_neuro_engine.py  —  VP Neuro upgrade engine (deterministic, modular)

ONE substrate, many modules. Every cell here is the SAME R19 bistable switch
(the jamming-lattice primitive that also writes DNA genes); a neuron is that
switch plus a SLOW RECOVERY (FitzHugh-Nagumo) -> a low-frequency relaxation
oscillator. Modules exchange typed messages over a bus and react.

The closed sensorimotor loop:

   stimulus (light/sound/odor/touch)  --emerge-->  receptor (transduce -> spikes)
        --ionic axon (NOT light)-->  cerebrum (E/I bands, theta/gamma)
        --descending command-->  cerebellum (supervised error learning)
        --motor command-->  muscle (recruitment + force-frequency = force)
        --stretch feedback (reflex arc)-->  back to receptor.

GUARDRAILS (retired in neuro 09 — never revived here):
  * the axon is NOT an optical fibre: conduction is 0.5-120 m/s ionic switching,
    ~10^6x slower than light. Light appears ONLY as an external stimulus.
  * low-frequency sums do NOT become "energy -> information": energy is the
    price of switching (ion pump), not information. A linear sum stays low-freq.
  * no DNA phase memory, no "vortex field".

Grades (honest, per VP-SPEC C3):  [F] forced  ·  [V] simulation-verified  ·
  [O] open (absolute magnitude needs external calibration; reason stated inline).

stdlib + numpy. Deterministic: seed fixed; 2x run -> identical sha256.
"""

import numpy as np
import math

SEED = 19
def seed_everything(seed=SEED):
    np.random.seed(seed)

# ===========================================================================
#  R19 — the shared bistable switch  (the jamming/DNA/neuron primitive)
#     ds/dt = g*s - s^3 + h     (double well; g sets the threshold SCALE)
# ===========================================================================
def sdot(s, g, h):
    return g * s - s ** 3 + h

def spinodal(g):
    """|h| past which the opposite basin disappears -> the flip is DISCONTINUOUS."""
    return 2.0 * (g / 3.0) ** 1.5

def barrier(g):
    """g^2/4 : energy barrier between the two basins (state stability)."""
    return g * g / 4.0

def settle(g, h, s0=None, n=1500, dt=0.02):
    """Integrate the R19 field from s0 to its steady state under fixed drive h."""
    s = (-math.sqrt(g) if g > 0 else 0.0) if s0 is None else s0
    for _ in range(n):
        s += dt * sdot(s, g, h)
    return s

def is_on(g, h, s0=None):
    return settle(g, h, s0) > 0.0


def dwell(g, brake, K=0.6):
    """DWELL: how long the switch runs ∝ γ^1.5 (DNA §5), throttled by a growth
    brake. Sets RELATIVE organ size — the order/direction is forced [F], the
    absolute magnitude is calibration [O]."""
    return (g ** 1.5) / (K + brake)


class Organ:
    """An organ EMERGED from its master gene's measured γ (READ-ONLY). The R19
    switch sets a DISCONTINUOUS presence threshold (spinodal); STATE (the master
    cis drive) decides presence — an intact downstream pathway with the master
    OFF still yields ABSENCE ('parts present ≠ trait'). The functional spinodal
    orders organs in developmental time; DWELL ∝ γ^1.5 sets relative size.
    γ is measured and never fitted; only STATE and size move.  [F] form/order."""
    def __init__(self, name, gamma, master="", partners=(), layer=""):
        self.name, self.g = name, float(gamma)
        self.master, self.partners, self.layer = master, tuple(partners), layer
        self.spinodal = spinodal(self.g)
        self.barrier = barrier(self.g)
    def present(self, cis_drive):
        """Present only if the master cis drive clears the γ-set threshold."""
        return is_on(self.g, cis_drive)
    def functional_spinodal(self):
        """Drive needed to switch the organ ON — the developmental-order key."""
        return self.spinodal
    def size(self, brake=0.5):
        return dwell(self.g, brake)


# ===========================================================================
#  Neuron — R19 switch + SLOW recovery  (FitzHugh-Nagumo)  => low frequency
# ===========================================================================
class Neuron:
    """A neuron is the R19 switch (fast) with a slow recovery w. Because the
    recovery sets the period, the intrinsic rhythm is far slower than the switch
    timescale -> the substrate speaks at LOW FREQUENCY (neuro 02).  [F]/[V]"""
    def __init__(self, gamma=1.0, tau_f=1.0, tau_s=40.0, beta=0.5, name="neuron"):
        self.g, self.tau_f, self.tau_s, self.beta, self.name = gamma, tau_f, tau_s, beta, name

    def run(self, drive, E=1.0, I=1.0, T=4000.0, dt=0.05, s0=-1.0, w0=0.0):
        """drive: scalar bias h0 (or a length-T array). Returns membrane trace S."""
        n = int(T / dt)
        if np.isscalar(drive):
            drive = np.full(n, float(drive))
        else:
            drive = np.asarray(drive, float)
            n = len(drive)
        s, w = s0, w0
        S = np.empty(n)
        for i in range(n):
            s += dt * (E * (self.g * s - s ** 3) - I * w + drive[i]) / self.tau_f
            w += dt * (s - self.beta * w) / self.tau_s
            s = 12.0 if s > 12 else (-12.0 if s < -12 else s)
            S[i] = s
        return S, dt

    @staticmethod
    def spikes(S, thr=0.0):
        """Up-crossings of threshold = all-or-none spike times (indices)."""
        a = S > thr
        return np.where((~a[:-1]) & (a[1:]))[0] + 1

    @staticmethod
    def rate_hz(S, dt, thr=0.0):
        sp = Neuron.spikes(S, thr)
        dur = len(S) * dt
        return len(sp) / dur if dur > 0 else 0.0


def dominant_freq(S, dt):
    """Dominant rhythm (Hz) from the FFT of the membrane trace (DC removed)."""
    x = S - S.mean()
    n = len(x)
    f = np.fft.rfftfreq(n, d=dt)
    P = np.abs(np.fft.rfft(x)) ** 2
    P[0] = 0.0
    return float(f[np.argmax(P)])


# ===========================================================================
#  STIMULUS — emerge the external physical signal (light verified separately)
# ===========================================================================
class LightStimulus:
    """External light = the longitudinal lattice wave verified at c^2=B/rho, with
    the propagation-angle law sinχ=λ/(mD) (physics §10.9). It is the EXTERNAL
    drive to the eye; it is NOT neural conduction (guardrail).  [V]"""
    D = 4.852620477e-12  # rotation length (winding unit), metres
    def __init__(self, wavelength_nm, intensity=1.0):
        self.lam = wavelength_nm * 1e-9
        self.intensity = float(intensity)
    def angle_deg(self):
        r = self.lam / self.D
        m = math.ceil(r)
        return math.degrees(math.asin(r / m))
    def photon_eV(self):
        h, c, q = 6.62607015e-34, 299792458.0, 1.602176634e-19
        return h * c / self.lam / q
    def visible(self):
        return 380e-9 <= self.lam <= 700e-9

class WaveStimulus:
    """A low-frequency pressure wave (sound) on the SAME elastic medium, c=√(B/ρ).
    'Low-frequency emergence' here = a genuinely slow mechanical oscillation, NOT
    a low-freq sum masquerading as energy/information (guardrail).  [F]"""
    def __init__(self, freq_hz, amplitude=1.0):
        self.freq, self.amp = float(freq_hz), float(amplitude)
    def sample(self, T, dt):
        t = np.arange(0, T, dt)
        return self.amp * np.sin(2 * np.pi * self.freq * t)

class MoleculeStimulus:
    """Odorant/tastant: a ligand concentration (dimensionless).  [F]"""
    def __init__(self, concentration, kind="odor"):
        self.c, self.kind = float(concentration), kind

class TouchStimulus:
    """Mechanical indentation / temperature on skin (dimensionless).  [F]"""
    def __init__(self, pressure=0.0, temperature_C=32.0):
        self.p, self.T = float(pressure), float(temperature_C)

class StretchStimulus:
    """Muscle/tendon stretch — the proprioceptive drive (dimensionless). A
    lengthening of the muscle deflects the spindle's PIEZO2 channels. [F]"""
    def __init__(self, stretch=0.0):
        self.stretch = float(stretch)

class AccelStimulus:
    """Head acceleration / tilt along a hair-bundle axis (dimensionless, SIGNED).
    Drives the vestibular hair cell directionally — sign matters because the hair
    bundle is morphologically polarised (toward the kinocilium vs away). [F]"""
    def __init__(self, accel=0.0, axis="z"):
        self.accel, self.axis = float(accel), axis


# ===========================================================================
#  RECEPTORS — transduce a stimulus into a LOW-FREQUENCY spike train
#     pattern: stimulus -> graded receptor drive -> R19/FHN spikes -> low-pass
# ===========================================================================
class Receptor:
    """Base transducer. A stimulus sets a graded receptor potential that biases
    the spiking neuron along the MONOTONIC RISING EDGE of its firing window: in
    the dark/quiet the cell sits just below threshold (silent); stimulus
    depolarises it toward its optimal firing point, so a stronger stimulus gives
    MORE spikes. Coupling+recovery low-pass fast input into a slow signal (neuro
    02). Subclasses define a normalised stimulus magnitude in [0,1] only."""
    LOW, HIGH = -0.85, -0.05   # silent floor -> near-peak: FHN monotonic rising edge
    def __init__(self, gamma=1.0, gain=1.0, name="receptor"):
        self.neuron = Neuron(gamma=gamma, name=name)
        self.gain, self.name = gain, name
    def drive_from(self, stimulus):
        raise NotImplementedError                 # return normalised magnitude ~[0,1]
    def transduce(self, stimulus, T=2000.0, dt=0.05):
        s = max(0.0, min(1.0, self.gain * self.drive_from(stimulus)))  # graded potential
        h0 = self.LOW + s * (self.HIGH - self.LOW)
        S, dt = self.neuron.run(h0, T=T, dt=dt)
        return dict(drive=h0, graded=s, S=S, dt=dt,
                    rate_hz=Neuron.rate_hz(S, dt),
                    freq_hz=dominant_freq(S, dt),
                    spikes=Neuron.spikes(S))

class Photoreceptor(Receptor):
    """Vision. Light hyperpolarises the cell in the dark-current convention, but
    we report the downstream EXCITATORY drive to the bipolar/ganglion stage so a
    brighter, visible stimulus -> stronger drive -> faster low-freq spiking.
    Wavelength sets an opsin sensitivity weight (toy three-cone).  [V]/[O abs]"""
    CONES = {"S": 440.0, "M": 540.0, "L": 565.0}   # peak nm
    def __init__(self, cone="L", **kw):
        super().__init__(name=f"cone-{cone}", **kw)
        self.peak = self.CONES[cone]
    def sensitivity(self, lam_nm):
        return math.exp(-0.5 * ((lam_nm - self.peak) / 40.0) ** 2)  # gaussian opsin
    def drive_from(self, light: 'LightStimulus'):
        if not light.visible():
            return 0.0
        w = self.sensitivity(light.lam * 1e9)
        return light.intensity * w

class MechanoReceptor(Receptor):
    """Hearing/touch. Indentation or wave amplitude opens mechano-gated channels
    -> graded drive. For the ear we feed the wave's RMS amplitude.  [V]/[O abs]"""
    def drive_from(self, stim):
        if isinstance(stim, WaveStimulus):
            return stim.amp
        if isinstance(stim, TouchStimulus):
            return stim.p
        return float(stim)

class ChemoReceptor(Receptor):
    """Smell/taste. Ligand binding -> Hill-saturated drive (Kd=0.5).  [V]/[O abs]"""
    def drive_from(self, mol: 'MoleculeStimulus'):
        c = mol.c
        return c / (0.5 + c)

class Thermoreceptor(Receptor):
    """Skin temperature. Drive rises with |T-32C| deviation from neutral.  [V]/[O abs]"""
    def drive_from(self, touch: 'TouchStimulus'):
        return abs(touch.T - 32.0) / 15.0

class Nociceptor(Receptor):
    """Pain. A HIGH-threshold polymodal nociceptor: SILENT for innocuous stimuli,
    fires only ABOVE a noxious threshold — the defining, measured property that
    separates pain from touch/warmth (a low-threshold thermoreceptor responds to a
    35C warmth a nociceptor ignores). Heat arm: TRPV1 opens above ~43C (Caterina
    1997, measured); mechanical arm: rectified above a noxious indentation. The
    polymodal cell fires if EITHER arm is driven. The threshold ORDER (nociceptor
    HIGH vs mechano/thermo LOW) is forced/measured [F]; absolute firing magnitude
    and the absolute mechanical threshold are [O].  master PRDM12 · Nav1.7 (SCN9A)."""
    T_NOX = 43.0     # TRPV1 heat-activation threshold, C (Caterina 1997 — MEASURED, cited)
    P_NOX = 0.5      # noxious mechanical threshold (normalised; the absolute value is [O])
    def drive_from(self, touch: 'TouchStimulus'):
        heat = max(0.0, (touch.T - self.T_NOX) / 12.0)   # 43C->55C maps 0->1 (silent below 43C)
        mech = max(0.0, (touch.p - self.P_NOX) / 0.5)    # rectified above the noxious threshold
        return min(1.0, heat + mech)                      # polymodal: either arm drives it

class Proprioceptor(Receptor):
    """Proprioception — the muscle spindle's Ia afferent. PIEZO2 stretch-gated
    channels make the firing rise with muscle stretch (Woo 2015; in humans loss of
    PIEZO2 abolishes proprioception and touch, Chesler 2016). The spindle's output
    feeds the stretch-reflex arc (ReflexArc), so the loop closes onto an ACTUAL
    afferent organ rather than an abstract 'stretch'. Firing rises monotonically
    with stretch [V]; absolute gain is [O].  master RUNX3 · identity ETV1/NTRK3."""
    def drive_from(self, stretch: 'StretchStimulus'):
        return max(0.0, stretch.stretch)                  # Ia firing ∝ stretch (rectified)

class VestibularReceptor(Receptor):
    """Balance / acceleration — the vestibular hair cell. Hair cells are
    morphologically polarised, so deflection TOWARD the kinocilium depolarises
    (more firing) and AWAY hyperpolarises (less firing) about a resting discharge
    (Hudspeth). The response is therefore SIGNED — equal-magnitude accelerations of
    opposite direction give different firing — unlike unsigned pressure. The
    directionality is the verified claim [V]; the absolute resting rate and gain are
    [O].  master ATOH1 (hair-cell master, Bermingham 1999) · otolith OTOP1/OTOG."""
    REST = 0.5       # resting discharge sets the operating point (a model choice; absolute [O])
    def drive_from(self, acc: 'AccelStimulus'):
        return self.REST + 0.5 * acc.accel                # SIGNED about rest (base clamps to [0,1])


# ===========================================================================
#  AXON — ionic conduction (NOT optical). Carries a spike train with delay.
# ===========================================================================
class Axon:
    """Conduction is ionic R19 switching: 0.5-120 m/s, ~10^6x SLOWER than light.
    Modelled as a pure transport delay on the spike train (myelination = speed).
    The axon is NOT a light pipe (retired guardrail).  [F]"""
    def __init__(self, length_m=0.5, speed_mps=60.0):
        self.length, self.speed = length_m, speed_mps
    def delay_ms(self):
        return 1000.0 * self.length / self.speed
    def conduct(self, spikes_idx, dt):
        d = int(round(self.delay_ms() / 1000.0 / dt))
        return spikes_idx + d, d


# ===========================================================================
#  CEREBRUM — E/I network; tau_inh sets the band; theta gates gamma; capacity θ/γ
# ===========================================================================
class Cerebrum:
    """An excitatory/inhibitory population. The inhibitory time-constant tau_inh
    sets the band: one circuit walks δ->θ->γ as tau_inh shortens (neuro 03). A
    theta frame of gamma slots makes working-memory capacity = θ/γ ratio ≈ 7±2 —
    the ONE causally-confirmed link (tACS).  [F]/[V] structure; [O] absolute Hz."""
    def __init__(self, gamma=1.0):
        self.unit = Neuron(gamma=gamma, name="ei-unit")
    def band(self, tau_inh, drive=0.0, T=4000.0, dt=0.05):
        # faster inhibition (smaller tau_inh) -> faster recovery -> higher band.
        # tau_inh plays the role of the slow (inhibitory) recovery time-constant.
        self.unit.tau_s = float(tau_inh)
        S, dt = self.unit.run(drive, E=1.0, I=1.0, T=T, dt=dt, s0=-1.0)
        return dominant_freq(S, dt), S, dt
    def working_memory_capacity(self, f_theta, f_gamma):
        """capacity = number of gamma cycles nested in one theta cycle = γ/θ."""
        return f_gamma / f_theta
    def integrate(self, afferent_rate_hz, tau_inh=20.0):
        """Afferent sensory rate biases the population drive (kept inside the
        oscillatory window); return band + a scalar 'percept' read-out."""
        drive = float(np.clip(-0.4 + 0.03 * afferent_rate_hz, -0.6, 0.3))
        self.unit.tau_s = float(tau_inh)
        S, dt = self.unit.run(drive, T=4000.0, dt=0.05)
        return dict(freq_hz=dominant_freq(S, dt),
                    percept=float(np.mean(S[len(S)//2:])),
                    drive=drive, S=S, dt=dt)


# ===========================================================================
#  CEREBELLUM — supervised error learning (climbing-fibre delta rule)
# ===========================================================================
class Cerebellum:
    """Error-based supervised learning, SEPARATE from the hippocampal store. A
    teaching signal (climbing fibre) drives a delta-rule reduction of motor error
    toward zero; removing the perturbation gives an opposite-sign after-effect
    (neuro 08).  [V] direction; [O] absolute gain."""
    def __init__(self, lr=0.12):
        self.w = 0.0          # learned forward-model correction
        self.lr = lr
        self.history = []
    def step(self, target, perturbation=0.0):
        command = self.w
        produced = command + perturbation          # plant adds the perturbation
        error = target - produced                  # climbing-fibre error
        self.w += self.lr * error                  # delta rule
        self.history.append(error)
        return command, produced, error
    def adapt(self, target, perturbation, trials=60):
        errs = [self.step(target, perturbation)[2] for _ in range(trials)]
        return np.array(errs)
    def after_effect(self, target, trials=20):
        """Remove the perturbation -> the learned w overshoots (opposite sign)."""
        pre = self.w
        outs = [self.step(target, 0.0)[1] for _ in range(trials)]
        return np.array(outs), pre


# ===========================================================================
#  MUSCLE — motor unit: size-principle recruitment + force-frequency
# ===========================================================================
class Muscle:
    """The final common path. Recruitment follows the size principle (small units first;
    Henneman 1965; Fuglevand-Winter-Patla 1993); within a unit, force rises with firing rate
    from twitch toward tetanus. The twitch->tetanus RATIO is a LOCKED MEASURED input
    (representative ~3.9x; the precise value is muscle/species/temperature dependent and is
    [O]) — it is not derived here. The recruitment ORDER and the monotone force rise ARE
    derived. Low force = recruitment, high force = rate — a dual code (neuro 08).  [V] order/
    shape; [O] absolute magnitudes."""
    def __init__(self, n_units=20, tetanus_ratio=3.9):
        # motor-unit size set: ascending small->large twitch forces, a representative MEASURED
        # range (Fuglevand-Winter-Patla 1993). The ORDER is forced; absolute forces/counts [O].
        self.sizes = np.linspace(1.0, 8.0, n_units)   # ascending unit sizes (small->large)
        self.tet = tetanus_ratio                      # LOCKED measured twitch->tetanus ratio ([O] precise)
    def recruited(self, drive):
        return self.sizes[self.sizes <= 1.0 + drive * 7.0]
    def force(self, drive, rate_frac=0.5):
        """drive in [0,1] recruits units up to a threshold; rate_frac sets the
        twitch->tetanus gain on recruited units."""
        ff = 1.0 + (self.tet - 1.0) * np.clip(rate_frac, 0, 1)
        return float(np.sum(self.recruited(drive)) * ff)
    def max_force(self):
        return self.force(1.0, 1.0)
    def recruitment_curve(self, drives, rate_frac=0.5):
        return [self.force(d, rate_frac) for d in drives]
    def force_frequency_curve(self, rates, drive=1.0):
        return [self.force(drive, r) for r in rates]
    def recruitment_order_ascending(self, drives):
        """returns True if units are recruited small-first (the size principle)."""
        order = []
        for d in drives:
            n = len(self.recruited(d))
            order.append(n)
        return all(order[i] <= order[i+1] for i in range(len(order)-1))


class ReflexArc:
    """The minimal sensorimotor loop: a stretch raises sensory drive, the spinal
    loop opposes the length change with NEGATIVE feedback (≈9.4× correction),
    homologous to the hypothalamic setpoint (neuro 07/08).  [V] direction."""
    def __init__(self, gain=9.4):
        self.gain = gain
    def correct(self, stretch):
        return -self.gain * stretch     # opposes the perturbation
    def closed_loop_error(self, disturbance):
        """Steady-state length error under a disturbance, with vs without the
        reflex. Negative feedback divides the error by (1+gain)."""
        open_err = disturbance
        closed_err = disturbance / (1.0 + self.gain)
        return dict(open=open_err, closed=closed_err,
                    rejection=open_err / closed_err)


# ===========================================================================
#  BUS — typed messages; modules exchange data and react
# ===========================================================================
class Bus:
    """A tiny deterministic message bus. Modules publish typed payloads; the loop
    reads them in order. This is the 'modules exchange data and react' fabric."""
    def __init__(self):
        self.log = []
    def send(self, src, dst, kind, payload):
        self.log.append(dict(src=src, dst=dst, kind=kind, payload=payload))
        return payload
    def trace(self):
        return [(m["src"], "→", m["dst"], m["kind"]) for m in self.log]
